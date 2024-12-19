import minio.datatypes

from abc import ABC, abstractmethod
from typing import Any

class DatabaseDriver(ABC):
    @abstractmethod
    def get_all(self) -> list[Any]:
        pass

    @abstractmethod
    def get_object(self, bucket_name: str, object_name: str) -> Any:
        pass

    @abstractmethod
    def get_all_objects(
        self, bucket_name: str, amount: int
    ) -> tuple[bool, list[minio.datatypes.Object] | str]:
        pass

    @abstractmethod
    def put_object(
        self, bucket_name: str, object_name: str, object_content: bytes
    ) -> None:
        pass
