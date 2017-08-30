"""

hcamerge: Combines gene cell matrices in a study into a single file.

Usage:

`hca-merge bucket-id`

This will download the slices from each study and merge them into a single
file, and deposit that file in the bucket.

"""

import argparse
import tempfile
import shutil


def merge_study(bucket_id, path):
    """
    Will download the slices for each study and merge them, depositing the
    resulting file in the bucket.

    :param bucket_id:
    :param path:
    :return:
    """
    # run hca filter for each bucket ID in the manifest JSON

    # download the TSV from bucket_id for each

    # write the results to temporary directory

    # upload the merged tsv to s3

    return

def main(args=None):
    """
    The console script that coordinates filtering samples and adding them
    to the to-bucket.

    :param args:
    :return:
    """
    parser = argparse.ArgumentParser(
        description='Merge gene cell matrices in a study into a single file.')
    parser.add_argument("bucket_id", type=str,
                        help="The ID of the study we would like to merge.")

    parsed = parser.parse_args(args)
    print(parsed)

    temp_path = tempfile.mkdtemp()
    merge_study(parsed.bucket_id, temp_path)
    shutil.rmtree(temp_path)
