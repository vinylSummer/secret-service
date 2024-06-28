from io import BytesIO

import minio
from minio import Minio

from internal.errors.errors import KeyDoesNotExistError, StorageServiceError
from internal.storage_service_client_interface import StorageServiceClientInterface


class MinIOStorageServiceClient(StorageServiceClientInterface):
    client: Minio
    bucket: str

    def __init__(
            self,
            s3_endpoint: str,
            s3_access_key: str,
            s3_secret_key: str,
            s3_bucket: str,
    ):
        client = Minio(
            endpoint=s3_endpoint,
            access_key=s3_access_key,
            secret_key=s3_secret_key,
        )
        self.client = client
        self.bucket = s3_bucket

        self.init_bucket()

    def init_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def create_data(self, key: str, data: bytes):
        try:
            self.client.put_object(
                self.bucket,
                key,
                BytesIO(data),
                len(data)
            )
        except minio.error.MinioException as e:
            raise StorageServiceError(e)

    def retrieve_data(self, key: str) -> bytes:
        if not self._object_exists(key):
            raise KeyDoesNotExistError()
        try:
            response = self.client.get_object(
                self.bucket,
                key
            )
            return response.data
        except minio.error.MinioException as e:
            raise StorageServiceError(e)
        finally:
            response.close()
            response.release_conn()

    def _object_exists(self, key: str) -> bool:
        try:
            _ = self.client.stat_object(
                self.bucket,
                key
            )
            return True
        except minio.error.S3Error:
            return False

    def delete_data(self, key: str):
        if not self._object_exists(key):
            raise KeyDoesNotExistError()
        try:
            self.client.remove_object(
                self.bucket,
                key,
            )
        except minio.error.MinioException as e:
            raise StorageServiceError(e)
