import pandas as pd 
from config.settings import RAW_DIR, BASE_DIR
from logging.handlers import RotatingFileHandler
import logging


LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

terminal_handler = logging.StreamHandler()
terminal_handler.setLevel(logging.WARNING)
terminal_handler.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))

file_handler = RotatingFileHandler(
    filename=LOGS_DIR / "prismbi.log",
    maxBytes=5 * 1024 * 1024, 
    backupCount=3
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(filename)s: %(lineno)d |%(message)s",
datefmt="%Y-%m-%d %H:%M:%S"
))
logger.addHandler(terminal_handler)
logger.addHandler(file_handler)


def load_excel(filename):

    file_path = RAW_DIR / filename 
    logger.info("Attempting to read file: %s", file_path)

    try:
        df = pd.read_excel(file_path)
        logger.info("File successfully read: %s — %d rows", filename, len(df))
        return df
    except FileNotFoundError:
        logger.error("File not found: %s", file_path)
    except UnicodeDecodeError:
        logger.error("File could not be read, format may be invalid: %s", file_path)
    except Exception:
        logger.exception("Unexpected error while reading file: %s", file_path)
    return None