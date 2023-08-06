import logging
import logging.config
import pathlib

from datetime import date

from sqlalchemy import create_engine, Engine

from alembic.config import Config
from alembic import command


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)


def create_tmp_db_engine() -> Engine:
    """
    Creates a temporary db with the latest migrations and returns an engine for it.
    The db content can only be accessed using the returned engine.
    """

    # Remove any pre-existing tmp db file
    pathlib.Path("/tmp/tmptest.db").unlink(missing_ok=True)

    # Migrate db to latest revision
    alembic_cfg = Config("alembic_test.ini")
    command.upgrade(alembic_cfg, "head")

    return create_engine("sqlite:////tmp/tmptest.db", echo=True)


def isodate(iso_format_date: str) -> date:
    return date.fromisoformat(iso_format_date)
