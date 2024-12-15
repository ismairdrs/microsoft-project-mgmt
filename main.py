import os

import uvicorn

if __name__ == "__main__":
    application_path = os.getenv("APPLICATION_PATH", "microsoft.api.main:app")
    application_port = int(os.getenv("APPLICATION_PORT", 8000))
    application_bind = os.getenv("APPLICATION_BIND", "0.0.0.0")

    uvicorn.run(application_path, host=application_bind, port=application_port)
