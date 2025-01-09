import random
from typing import Iterator

from urllib3 import BaseHTTPResponse
from images.database_driver import DatabaseDriver
from minio import Minio
from minio.datatypes import Bucket
from minio.datatypes import Object as MinioObject
from images.exceptions import EmptyBucketException, BucketDoesNotExistException


class MinioDatabaseDriverImpl(DatabaseDriver):
    _minio_db: Minio

    def __init__(self, database: Minio) -> None:
        self._minio_db = database

    def get_all(self) -> list[Bucket]:
        return self._minio_db.list_buckets()

    def get_all_objects(self, bucket_name: str, amount: int) -> list[MinioObject]:
        if amount > 100:
            amount = 100

        if self._minio_db.bucket_exists(bucket_name):
            minio_objects: list[MinioObject] = []
            minio_objects_iter: Iterator[MinioObject] = self._minio_db.list_objects(
                bucket_name
            )

            ticker: int = 0
            for minio_object in minio_objects_iter:
                if ticker >= amount:
                    break
                minio_objects.append(minio_object)
                ticker += 1

            return minio_objects
        else:
            raise BucketDoesNotExistException()

    def get_object(self, bucket_name: str, object_name: str) -> BaseHTTPResponse | None:
        responce = None

        try:
            responce = self._minio_db.get_object(
                bucket_name=bucket_name, object_name=object_name
            )
        finally:
            if responce:
                responce.close()
                responce.release_conn()
            return responce

    def put_object(
        self, bucket_name: str, object_name: str, object_content: bytes
    ) -> None:
        pass

    def get_random_object(self, bucket_name: str) -> BaseHTTPResponse:
        pass

    #     is_responce: bool
    #     all_objects_in_bucket: list[MinioObject] | str

    #     is_responce, all_objects_in_bucket = self.get_all_objects()

    #     if is_responce and all_objects_in_bucket and not isinstance(all_objects_in_bucket):

    #     elif is_responce and not all_objects_in_bucket:
    #         raise EmptyBucketException("The bucket is empty, nothing to choose from")

    #     else:
    #         raise BucketDoesNotExistException(
    #             "The bucket with that name doesn't seem to be existent"
    #         )
