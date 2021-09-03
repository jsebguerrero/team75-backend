from dotenv import load_dotenv
from dotenv_settings_handler import BaseSettingsHandler
import os
__all__ = ("settings",)
#load .env file injected via docker or the existing one
load_dotenv()

#settings
class Settings(BaseSettingsHandler):
    port = os.getenv('PORT')
    host = os.getenv('HOST')
    spark = os.getenv('SPARK')
    workers = os.getenv('WORKERS')
    dbconn = os.getenv('DB')
    s3bucket = os.getenv('BUCKET_NAME')
    region = os.getenv('REGION')
    class Config:
        case_insensitive = True


settings = Settings()
