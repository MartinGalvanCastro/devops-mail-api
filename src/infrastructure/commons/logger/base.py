import logging

from src.infrastructure.commons.settings.base import settings


def setup_logging() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL, format="%(levelname)s:     %(message)s"
    )
    logging.getLogger("sqlalchemy.engine.Engine").handlers = [logging.NullHandler()]
