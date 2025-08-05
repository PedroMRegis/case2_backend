from dotenv import load_dotenv
import os
from mongoengine import connect
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import quote_plus

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PWD = os.getenv("MONGO_PWD")



connect(db="todo_app", host=f"mongodb+srv://{MONGO_USER}:{MONGO_PWD}@clustercase2.zov6ja1.mongodb.net/todo_app?retryWrites=true&w=majority")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

