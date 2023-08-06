from contextlib import contextmanager
from os import path

import pytest
from google.cloud import storage

PROJECT_ID = 'data-science-360fc06f'
TEMP_DATASET = 'temp_1day'
TEMP_BUCKET = 'data_science_temp_30days'


@pytest.fixture(scope='module')
def storage_client():
    return storage.Client(PROJECT_ID)


@contextmanager
def temp_files_to_gcs(storage_client, bucket_name, local_dirpath, filenames):
    bucket = storage_client.bucket(bucket_name)
    try:
        for filename in filenames:
            blob = bucket.blob(filename)
            with open(path.join(local_dirpath, filename), 'rb') as fileobj:
                blob.upload_from_file(fileobj)
        yield
    finally:
        for filename in filenames:
            blob = bucket.blob(filename)
            blob.delete()
