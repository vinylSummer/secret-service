import logging
import os
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI

from internal.image_service.image_service import ImageService
from internal.routers import images
from internal.storage_service_client.storage_service_client import StorageServiceClient
from internal.storage_service_client_interface import StorageServiceClientInterface

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
logger.info("Successfully initialized FastAPI app")

storage_service_endpoint: str = os.getenv("S3_ENDPOINT")
assert storage_service_endpoint is not None, "S3_ENDPOINT environment variable must be set"
storage_service_client: StorageServiceClientInterface = StorageServiceClient(
    storage_service_endpoint=storage_service_endpoint,
)
logger.info("Successfully initialized S3 client")

service = ImageService(
    storage_service_client=storage_service_client,
)
logger.info("Successfully initialized image service")

image_router = images.get_router(
    image_service=service,
)

app.include_router(image_router)
logger.info("Successfully included image service router, starting up..")
