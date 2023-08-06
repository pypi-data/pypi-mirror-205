import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    def __init__(self, logger_name: str) -> None:
        self.logger_name = logger_name
        super().__init__()

    def emit(self, record) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.patch(lambda record: record.update(name=self.logger_name)).opt(
            depth=depth, exception=record.exc_info
        ).log(level, record.getMessage())
