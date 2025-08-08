from dotenv import load_dotenv
import os
from mongoengine import connect
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from importlib import import_module
import glob

load_dotenv() 
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PWD = os.getenv("MONGO_PWD")



connect(db="teste", host=f"mongodb+srv://{MONGO_USER}:{MONGO_PWD}@clustercase2.zov6ja1.mongodb.net/teste?retryWrites=true&w=majority")

app = FastAPI()
@app.get("/")
def test():
    return {"status": "OK v2 (3)"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

working_directory = os.path.dirname(os.path.abspath(__file__))
use_cases_directory = os.path.join(working_directory, "use_cases")
routes = glob.glob(os.path.join(use_cases_directory, "**/index.py"), recursive=True)

for route in routes:
    relative_path = os.path.relpath(route, working_directory)
    module_name = os.path.splitext(relative_path)[0].replace(os.path.sep, '.')

    try:
        print(f"Importing module: {module_name}")
        module = import_module(module_name)
        if hasattr(module, 'router'):
            app.include_router(module.router)
    except ModuleNotFoundError as e:
        print(f"Erro ao importar módulo {module_name}: {e}")

