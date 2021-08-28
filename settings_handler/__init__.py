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
    workers = os.getenv('WORKERS')
    class Config:
        case_insensitive = True


settings = Settings()
