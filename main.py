import os
import uvicorn
from dotenv import load_dotenv

from app.api.server import app  # noqa: F401 — exposes `app` for `uvicorn main:app`

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(app, host=host, port=port, reload=True)
