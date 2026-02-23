import os

MONGO_URI: str | None = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI no está definida en el entorno")