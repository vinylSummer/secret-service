import logging
import os
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI

from internal.routes import data
from internal.storage_service.storage_service import StorageService
from internal.storage_service_client.minio.minio_storage_service_client import MinIOStorageServiceClient
from internal.storage_service_client_interface import StorageServiceClientInterface
from internal.storage_service_interface import StorageServiceInterface

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True
)
logger = logging.getLogger(__name__)

if not os.path.isfile("./.env") and os.path.isfile("./.env.example"):
    shutil.copyfile("./.env.example", "./.env")
    # TODO: decide if this should be a warning or not
    logger.info("Created .env file with default values from .env.example")

load_dotenv(
    dotenv_path="./.env",
    override=False,
)
logger.info("Loaded environment variables from .env file")

log_level = os.getenv('LOG_LEVEL', 'INFO')
logger.setLevel(log_level)


app = FastAPI()
logger.info("Initialized FastAPI app")

assert "S3_ENDPOINT" in os.environ, "S3_ENDPOINT environment variable must be set"
s3_endpoint = os.environ['S3_ENDPOINT']
assert "S3_ACCESS_KEY" in os.environ, "S3_ACCESS_KEY environment variable must be set"
s3_access_key = os.environ['S3_ACCESS_KEY']
assert "S3_SECRET_KEY" in os.environ, "S3_SECRET_KEY environment variable must be set"
s3_secret_key = os.environ['S3_SECRET_KEY']
assert "S3_BUCKET" in os.environ, "S3_BUCKET environment variable must be set"
s3_bucket = os.environ['S3_BUCKET']

s3_client: StorageServiceClientInterface = MinIOStorageServiceClient(
    s3_endpoint=s3_endpoint,
    s3_access_key=s3_access_key,
    s3_secret_key=s3_secret_key,
    s3_bucket=s3_bucket
)
logger.info("Initialized S3 client")

service: StorageServiceInterface = StorageService(
    storage_service_client=s3_client,
)
logger.info("Initialized S3 service")

router = data.get_router(service)
logger.info("Initialized data router")

app.include_router(router)
logger.info("Included data router, starting up..")
