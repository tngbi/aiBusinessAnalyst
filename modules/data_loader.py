
import pandas as pd
from utils.logger import logger
from config import SUPPORTED_FILE_TYPES, EXPECTED_COLUMNS


def load_excel(file):
    """Load an uploaded file (Excel or CSV) into a DataFrame."""
    try:
        filename = getattr(file, "name", "")
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns from {filename}")

        # Warn about missing expected columns
        missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
        if missing:
            logger.warning(f"Missing expected columns: {missing}")

        return df

    except Exception as e:
        logger.error(f"Failed to load file: {e}")
        raise ValueError(f"Could not read uploaded file: {e}")
