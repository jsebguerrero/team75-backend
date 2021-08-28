import uvicorn
from settings_handler import settings

import os
#select direct path to the app
PATH = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #invoke uvicorn to set up the ASGI for the app, this includes the port, host and # workers
    uvicorn.run(
        "app:app",
        host = settings.host,
        port = int(settings.port),
        reload = False,
        debug = False,
        workers = int(settings.workers)
    )
