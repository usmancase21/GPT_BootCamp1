from fastapi import FastAPI,Depends
from sqlmodel import SQLModel,Field,create_engine,Session,select
from typing import Optional

# Step 1 : Create Table Hero with Pydantic
class Hero(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name:str
    age: Optional[int] = None
# class Hero(SQLModel,table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     secret_name:str
#     age: Optional[int] = None

# Step 2 Database Connection with Conn String and Function
DB_URL = "postgresql://usman.qau12:4furb3sejMRK@ep-empty-darkness-04003085.ap-southeast-1.aws.neon.tech/empty?sslmode=require"
engine =create_engine("postgresql://usman.qau12:4furb3sejMRK@ep-empty-darkness-04003085.ap-southeast-1.aws.neon.tech/empty?sslmode=require")
def create_tables():
    SQLModel.metadata.create_all(engine)
# Step 3 Object of Faste API
app = FastAPI()

# Step 4 Startup function
@app.on_event("startup")
def on_startup():
    create_tables()

# Step 6 Getting Data from Table by GET Method
# Step 6.1 
@app.get("/heroes")
def get_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
# Step 6.3  Creating heros
@app.post("/heroes")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero