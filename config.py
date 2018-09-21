import os
from dotenv import load_dotenv

load_dotenv(dotenv_path = '.env')

KIOSK_KEY = os.getenv('KIOSK_KEY')
BASE_URL = os.getenv('BASE_URL')
