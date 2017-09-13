"""

hcamerge: Combines gene cell matrices in a study into a single file.

Usage:

`hca-merge bucket-id`

This will download the slices from each study and merge them into a single
file, and deposit that file in the bucket.

"""

import boto3

import argparse
import tempfile
import shutil

#  'davidcs-hca-release-2ecf2b1e7c8a19db785d'


def merge(outfilename, *infilenames):
    """
    Merges the infilenames into the outfilename in the same directory.

    :param outfilename:
    :param infilenames:
    :return:
    """
    print(outfilename)
    print(infilenames)
    with open(outfilename, 'w') as outfile:
        first = True
        for infilename in infilenames:
            with open(infilename) as infile:
                inner_first = True
                for line in infile:
                    if first and inner_first:
                        inner_first = False
                        first = False
                        if line.strip():
                            outfile.write(line)
                    elif inner_first:
                        inner_first = False
                    else:
                        if line.strip():
                            outfile.write(line)


def merge_study(bucket_id, path):
    """
    Will download the slices for each study and merge them, depositing the
    resulting file in the bucket.

    :param bucket_id:
    :param path:
    :return:
    """
    # run hca filter for each bucket ID in the manifest JSON
    s3 = boto3.client('s3')
    # download the TSV from bucket_id for each
    objects = [x['Key'] for x in s3.list_objects(Bucket=bucket_id)['Contents']]
    [s3.download_file(Bucket=bucket_id, Key=y, Filename=y) for y in objects]
    print([y for y in objects])
    # write the results to temporary directory
    merge(bucket_id, *objects)
    # upload the merged tsv to s3
    print(s3.upload_file(Filename=bucket_id, Bucket=bucket_id, Key=bucket_id))
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
