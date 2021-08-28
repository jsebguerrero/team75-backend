from app import app
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from app.version import VERSION
from starlette.middleware.cors import CORSMiddleware

#insert CORS to avoid errors with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#endpoints
@app.get('/health')
def health():
    return JSONResponse(content={'health': 'healthy', 'version': VERSION},
                        status_code=200)
