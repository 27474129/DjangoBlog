import os
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = os.path.join(Path(__file__).resolve().parent.parent, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


SECRET_KEY = os.getenv("SECRET_KEY")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
