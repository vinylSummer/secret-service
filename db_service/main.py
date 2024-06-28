import logging
import os
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI

from internal.database_service.database_service import DatabaseService
from internal.database_service_interface import DatabaseServiceInterface
from internal.meme_repo.sqlalchemy.postgres import MemeRepository
from internal.meme_repository_interface import MemeRepositoryInterface
from internal.postgres.connection import PostgresConnection
from internal.routers.meme import get_router

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True
)
logger = logging.getLogger(__name__)

if not os.path.isfile("./.env") and os.path.isfile("./.env.example"):
    shutil.copyfile("./.env.example", "./.env")
    logger.warning("Created .env file with default values from .env.example")

load_dotenv(
    dotenv_path="./.env",
    override=False,
)
logger.info("Loaded environment variables from .env file")

app = FastAPI()
logger.info("Initialized FastAPI app")

assert "DB_URL" in os.environ, "DB_URL is not set"
db_url = os.environ["DB_URL"]
db_connection = PostgresConnection(
    db_url=db_url,
)
logger.info("Database connection established")

# TODO: implement
meme_repository: MemeRepositoryInterface = MemeRepository(
    db_connection=db_connection,
)
logger.info("Database repository initialized")

db_service: DatabaseServiceInterface = DatabaseService(
    meme_repository=meme_repository,
)
logger.info("Database service initialized")

router = get_router(db_service)
logger.info("Database router initialized")

app.include_router(router)
logger.info("Database router included, starting up..")
