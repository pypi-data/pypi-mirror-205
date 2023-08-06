import logging
import sys
import time
import traceback

import boto3
import requests

from argparse import ArgumentParser
from pathlib import Path

from requests.auth import HTTPDigestAuth
from tqdm import tqdm

from rdflib import Dataset

# tqdm opt
TQDM_OPTS = {
    "ncols": 100,
    "ascii": True,
    "desc": "Uploading",
}


def redo_if_failure(call, max_redo=3, sleep_time=5, *args, **kwargs):
    """Redo a function if it fail, with a sleep time between each try"""
    i = 0
    while True:
        i += 1
        try:
            return call(*args, **kwargs)
        except Exception as e:
            if i == max_redo:
                raise (e)
            traceback.print_exc(file=sys.stdout)
            logging.debug(
                "Fail to execute {}. Retrying in {} sec...".format(
                    call.__name__, sleep_time
                )
            )
            time.sleep(sleep_time)
            sleep_time = sleep_time * 2
            continue  # redo


def delete_graph(virtuoso_url, virtuoso_user, virtuoso_password, graph_uri):
    logging.info(f"Deleting {graph_uri}…")
    response = requests.delete(
        f"{virtuoso_url}/sparql-graph-crud-auth?",
        auth=HTTPDigestAuth(virtuoso_user, virtuoso_password),
        params={"graph-uri": graph_uri},
    )
    if response.status_code == 404:
        logging.warning(f"Graph {graph_uri} doesn't exist")
    else:
        response.raise_for_status()
        # give virtuoso enough time to delete the graph
        time.sleep(3)


def upload_triples_to_graph(
    virtuoso_url,
    virtuoso_user,
    virtuoso_password,
    graph_uri,
    triples_str,
    filename,
):
    logging.info(f"Uploading {filename} into graph {graph_uri}")
    response = redo_if_failure(
        requests.post,
        3,
        5,
        f"{virtuoso_url}/sparql-graph-crud-auth",
        auth=HTTPDigestAuth(virtuoso_user, virtuoso_password),
        params={"graph-uri": graph_uri},
        data=triples_str,
        headers={"Content-type": "text/plain"},
    )
    response.raise_for_status()


def main():
    parser = ArgumentParser()
    parser.add_argument("--input-type", choices=["s3", "fs"], required=True)

    parser.add_argument("--s3-url", type=str)
    parser.add_argument("--s3-access-key", type=str)
    parser.add_argument("--s3-secret-key", type=str)
    parser.add_argument("--s3-bucket", type=str)
    parser.add_argument("--s3-dirs", type=str, nargs="+")

    parser.add_argument("--input-dirs", type=Path, nargs="+")

    parser.add_argument("--virtuoso-url", type=str, required=True)
    parser.add_argument(
        "--virtuoso-user", type=str, required=False, default="dba"
    )
    parser.add_argument(
        "--virtuoso-password", type=str, required=False, default="dba"
    )

    parser.add_argument("--rdf-graph", type=str, required=True)
    parser.add_argument("--delete-graph", action="store_true")
    parser.add_argument("--delete-only", action="store_true")

    parser.add_argument("-v", "--verbose", action="count", default=0)

    args = parser.parse_args()

    # Set verbosity
    VERBOSITY_MAPPING = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
    verbosity = args.verbose if args.verbose < 3 else 2
    logging.basicConfig(level=VERBOSITY_MAPPING[verbosity])

    # Delete graph before upload
    if args.delete_graph or args.delete_only:
        delete_graph(
            args.virtuoso_url,
            args.virtuoso_user,
            args.virtuoso_password,
            args.rdf_graph,
        )

    if args.input_type == "s3":
        s3_resource = boto3.resource(
            "s3",
            endpoint_url=args.s3_url,
            aws_access_key_id=args.s3_access_key,
            aws_secret_access_key=args.s3_secret_key,
        )

        # upload all files to graph
        if not args.delete_only:
            s3_bucket = s3_resource.Bucket(args.s3_bucket)

            # if no s3_dirs specified, we will loop on all files in the bucket
            prefixes = args.s3_dirs if args.s3_dirs else [""]

            for prefix in prefixes:
                # count object first
                total = sum(1 for _ in s3_bucket.objects.filter(Prefix=prefix))
                logging.info(
                    f"Upload {total} files form {args.s3_bucket}/{prefix} into"
                    f" {args.rdf_graph}"
                )
                # iter to upload
                for obj in tqdm(
                    s3_bucket.objects.all(), total=total, **TQDM_OPTS
                ):
                    rdf_string = obj.get()["Body"].read().decode("utf-8")

                    response = redo_if_failure(
                        requests.post,
                        3,
                        5,
                        f"{args.virtuoso_url}/sparql-graph-crud-auth",
                        auth=HTTPDigestAuth(
                            args.virtuoso_user, args.virtuoso_password
                        ),
                        params={"graph-uri": args.rdf_graph},
                        data=rdf_string.encode("utf-8"),
                        headers={"Content-type": "text/plain"},
                    )
                    response.raise_for_status()
    else:
        for input_dir in args.input_dirs:
            total = sum(
                1 for filepath in input_dir.rglob("*") if not filepath.is_dir()
            )
            logging.info(f"Upload {total} files form {input_dir}")
            for filepath in tqdm(
                input_dir.rglob("*"), total=total, **TQDM_OPTS
            ):
                if not filepath.is_dir():
                    if filepath.suffix in [".nquads", ".trig"]:
                        try:
                            dataset = Dataset()
                            dataset.parse(filepath)
                            for g in dataset.graphs():
                                delete_graph(
                                    args.virtuoso_url,
                                    args.virtuoso_user,
                                    args.virtuoso_password,
                                    g.identifier,
                                )
                                upload_triples_to_graph(
                                    args.virtuoso_url,
                                    args.virtuoso_user,
                                    args.virtuoso_password,
                                    g.identifier,
                                    g.serialize(format="ttl", encoding="utf-8"),
                                    filepath.name,
                                )
                        except Exception as e:
                            logging.error(
                                f"File {filepath} is supposed to be nquads"
                                f" format, but it isn't ({str(e)})"
                            )
                    else:
                        with filepath.open() as fp:
                            upload_triples_to_graph(
                                args.virtuoso_url,
                                args.virtuoso_user,
                                args.virtuoso_password,
                                args.rdf_graph,
                                fp.read().encode("utf-8"),
                                filepath.name,
                            )


if __name__ == "__main__":
    main()
