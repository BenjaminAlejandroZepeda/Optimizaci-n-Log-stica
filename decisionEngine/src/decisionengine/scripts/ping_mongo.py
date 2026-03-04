# scripts/ping_mongo.py
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure, ConfigurationError, PyMongoError

# Cargar .env si está disponible
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

uri = os.getenv("MONGO_URI")
if not uri:
    raise SystemExit(
        "✖ MONGO_URI no está definido.\n"
        "  - O exporta la variable antes de ejecutar (PowerShell):\n"
        '      $env:MONGO_URI="mongodb+srv://USER:PASSWORD@cluster.mongodb.net/?appName=App&authSource=admin"\n'
        "  - O crea un .env con MONGO_URI=... y añade python-dotenv."
    )

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    resp = client.admin.command("ping")
    print("✔ Ping OK:", resp)
    print("Pinged your deployment. You successfully connected to MongoDB!")
except OperationFailure as e:
    print("✖ OperationFailure (autenticación/roles/authSource):", e)
except ConfigurationError as e:
    print("✖ ConfigurationError (URI mal formada/opciones):", e)
except PyMongoError as e:
    print("✖ PyMongoError:", e)
except Exception as e:
    print("✖ Error desconocido:", e)