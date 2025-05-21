from dotenv import load_dotenv
import os
from logger import get_logger

logger = get_logger(__name__)

load_dotenv()

SECRET = os.environ.get('SECRET')
API_URL = os.environ.get("API_URL")
TG_SECRET = os.environ.get("TG_KEY")

logger.debug(f'System creds:{SECRET, API_URL, TG_SECRET}')