from typing import List
import google.cloud.storage


def list_files_in_gcloud_bucket(bucket_name: str, prefix: str = None) -> List[str]:
    """
    Returns a list of the files (filenames) present in a google cloud bucket

    Parameters
    ----------
    bucket_name: str
        The name of the google cloud bucket
    prefix: str, optional (default=None)
        If present, only returns files whose path starts with the given prefix

    Returns
    -------
    List[str]
        List of filenames in the google cloud bucket (file pathes)
    """
    storage_client = google.cloud.storage.Client()
    if prefix is not None:
        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    else:
        blobs = storage_client.list_blobs(bucket_name)
    all_filenames = []
    for blob in blobs:
        all_filenames.append(blob.name)

    return all_filenames
