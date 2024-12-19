from typing import Iterator

from urllib3 import BaseHTTPResponse
from db.database_driver import DatabaseDriver
from minio import Minio
from minio.datatypes import Bucket
from minio.datatypes import Object as MinioObject


class MinioDatabaseDriverImpl(DatabaseDriver):
    _minio_db: Minio

    def __init__(self, database: Minio) -> None:
        self._minio_db = database

    def get_all(self) -> list[Bucket]:
        return self._minio_db.list_buckets()

    def get_all_objects(
        self, bucket_name: str, amount: int
    ) -> tuple[bool, list[MinioObject] | str]:
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

            return True, minio_objects
        else:
            return False, f"Bucket {bucket_name} doesn't exist"

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
