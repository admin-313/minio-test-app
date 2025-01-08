import os
import uvicorn

from minio import Minio
from dotenv import load_dotenv
from urllib3 import BaseHTTPResponse
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from minio.datatypes import Object as MinioObject
from fastapi.middleware.cors import CORSMiddleware
from images.minio.minio_database_driver_impl import MinioDatabaseDriverImpl
from images.exceptions import EmptyBucketException, BucketDoesNotExistException

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MINIO_DB = Minio(
    # CHANGE CERTIFICATE CHECK TO TRUE IN PROD!!!!
    endpoint=MINIO_PATH,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    cert_check=False,
)

minio_driver = MinioDatabaseDriverImpl(MINIO_DB)


@app.get("/bucket/{bucket_name}/random")
async def read_random_item(bucket_name: str) -> StreamingResponse:
    try:
        pass
    except EmptyBucketException:
        raise HTTPException(
            status_code=404, detail="The bucket you have requested seems to be empty"
        )

    except BucketDoesNotExistException:
        raise HTTPException(
            status_code=404, detail="The bucket you have requested doesn't exist"
        )
    except:
        raise HTTPException(status_code=500, detail="Internal server error")


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


@app.get("/bucket/all")
async def read_minio() -> list[str]:
    return [bucket.name for bucket in minio_driver.get_all()]


@app.get("/bucket/{bucket_name}")
async def read_bucket(bucket_name: str, amount: int = 20) -> list[str | None]:
    try: 
        bucket_minio_objects: list[MinioObject] = (
            minio_driver.get_all_objects(bucket_name=bucket_name, amount=amount)
        )
        return [filename.object_name for filename in bucket_minio_objects]
    
    except BucketDoesNotExistException:
        raise HTTPException(status_code=404, detail="Specified bucket does not exist")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)