from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

fake_users_db = [{"user_name": "John"}, {"user_name": "Doh"}, {"user_name": "Baz"}]

class Users(BaseModel):
    name: str
    first_name: str
    date_of_birth: int
    email: Optional[str] = None


@app.get('/')
def read_root():
    return "bienvenue dans le programme"


@app.get('/users/{user_id}')
async def read_user(user_id: int):
    return {'message': f"identification de l'utilisateur {user_id}"}


@app.get("/users/")
async def list_users(skip: int = 0, limit: int = 10):
    return fake_users_db[skip : skip + limit]


@app.post("/users/")
async def create_users(users: Users):  # Le modèle Pydantic devient le body
    return {'message': users.model_dump_json()}