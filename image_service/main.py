import os
import logging

from fastapi import FastAPI

from internal.routers import images
from internal.image_service.image_service import ImageService
from internal.storage_service_client_interface import StorageServiceClientInterface


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True
)
logger = logging.getLogger(__name__)


app = FastAPI()
logger.info("Successfully initialized FastAPI app")

s3_endpoint: str = os.getenv("S3_ENDPOINT")
assert s3_endpoint is not None, "S3_ENDPOINT environment variable must be set"
# TODO: add real implementation
storage_service_client: StorageServiceClientInterface
logger.info("Successfully initialized S3 client")

service = ImageService()
logger.info("Successfully initialized image service")

image_router = images.get_router(
    image_service=service,
)

app.include_router(image_router)
logger.info("Successfully included image service router")
