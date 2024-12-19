import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from minio import Minio
from urllib3 import BaseHTTPResponse
from db.minio_database_driver_impl import MinioDatabaseDriverImpl
from minio.datatypes import Object as MinioObject
from dotenv import load_dotenv

load_dotenv()

MINIO_PATH = os.getenv("MINIO_PATH")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_TARGET_BUCKET_NAME = os.getenv("MINIO_TARGET_BUCKET_NAME")

if (
    not MINIO_PATH
    or not MINIO_ACCESS_KEY
    or not MINIO_SECRET_KEY
    or not MINIO_TARGET_BUCKET_NAME
):
    raise ValueError("The config is fucked up, exiting")


app = FastAPI()

MINIO_DB = Minio(
    # CHANGE CERTIFICATE CHECK TO TRUE IN PROD!!!!
    endpoint=MINIO_PATH,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    cert_check=False,
)

minio_driver = MinioDatabaseDriverImpl(MINIO_DB)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"hello": "World"}


@app.get("/bucket/{bucket_name}/{object_name}")
async def read_item(bucket_name: str, object_name: str) -> StreamingResponse:
    file: BaseHTTPResponse | None = minio_driver.get_object(bucket_name, object_name)

    if file:
        return StreamingResponse(
            content=file,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={object_name}"},
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"{object_name} wasn't found in {bucket_name}"
        )


@app.get("/bucket/{bucket_name}")
async def read_bucket(bucket_name: str, amount: int = 20) -> list[str | None]:
    bucket_minio_objects: tuple[bool, list[MinioObject] | str] = (
        minio_driver.get_all_objects(bucket_name=bucket_name, amount=amount)
    )

    if not bucket_minio_objects[0]:
        raise HTTPException(status_code=404, detail=bucket_minio_objects[1])

    elif bucket_minio_objects[0] and isinstance(bucket_minio_objects[1], list):
        return [minio_object.object_name for minio_object in bucket_minio_objects[1]]
    else:
        raise HTTPException(status_code=500)


@app.get("/minio")
async def read_minio() -> list[str]:
    return [bucket.name for bucket in minio_driver.get_all()]
