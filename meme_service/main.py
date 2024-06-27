import logging
import os
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI

from internal.routers import meme
from internal.meme_service_interface import MemeServiceInterface
from internal.meme_service.meme_service import MemeServiceV1
from internal.image_service_client_interface import ImageServiceClientInterface
from internal.image_service_client.image_service_client import ImageServiceClient
from internal.db_service_client_interface import DatabaseServiceClientInterface
from internal.db_service_client.db_service_client import DatabaseServiceClient

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

load_dotenv()
logger.info("Loaded environment variables from .env file")

log_level = os.getenv('LOG_LEVEL', 'INFO')
logger.setLevel(log_level)


app = FastAPI()
logger.info("Successfully initialized FastAPI app")

assert "IMAGE_SERVICE_ENDPOINT" in os.environ, "IMAGE_SERVICE_ENDPOINT environment variable must be set"

image_service_endpoint = os.environ["IMAGE_SERVICE_ENDPOINT"]
image_service_client: ImageServiceClientInterface = ImageServiceClient(
    image_service_endpoint=image_service_endpoint,
)
logger.info("Successfully initialized image service client")

assert "DB_SERVICE_ENDPOINT" in os.environ, "DB_SERVICE_ENDPOINT environment variable must be set"

database_service_endpoint = os.environ["DB_SERVICE_ENDPOINT"]
database_service_client: DatabaseServiceClientInterface = DatabaseServiceClient(
    db_service_endpoint=database_service_endpoint,
)
logger.info("Successfully initialized database service client")

service: MemeServiceInterface = MemeServiceV1(
    image_service_client=image_service_client,
    db_service_client=database_service_client,
)
logger.info("Successfully initialized Meme Service")

meme_router = meme.get_router(service)

app.include_router(meme_router)
logger.info("Successfully included meme service API router")
