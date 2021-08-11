import uvicorn
from settings_handler import settings

import os

PATH = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host = settings.host,
        port = int(settings.port),
        reload = False,
        debug = False,
        workers = int(settings.workers)
    )