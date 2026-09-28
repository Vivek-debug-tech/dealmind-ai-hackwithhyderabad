import logging
from hindsight_client import Hindsight
from pydantic import ValidationError
from .config import settings

logger = logging.getLogger(__name__)

# Verify API Key is present
if not settings.hindsight_api_key or settings.hindsight_api_key == "your_api_key_here":
    raise ValueError("HINDSIGHT_API_KEY environment variable is not set correctly.")

client = Hindsight(
    base_url=settings.hindsight_base_url,
    api_key=settings.hindsight_api_key
)

def get_hindsight_client() -> Hindsight:
    return client

def ensure_bank_exists():
    try:
        # We try to create the bank. If it already exists, Hindsight will typically 
        # either return the existing one or raise an error.
        client.create_bank(
            bank_id=settings.hindsight_bank_id,
            name="DealMind Memory Bank"
        )
        logger.info(f"Bank {settings.hindsight_bank_id} verified/created.")
    except Exception as e:
        # Check if the error indicates it already exists. If so, we can just log and proceed.
        # As we don't have exact exception details for 409 Conflict, we'll log it as info.
        logger.info(f"Bank {settings.hindsight_bank_id} creation returned: {e}. Assuming it exists.")

# Ensure bank is initialized when module is loaded.
ensure_bank_exists()
