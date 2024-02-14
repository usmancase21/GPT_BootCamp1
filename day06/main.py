from fastapi import FastAPI,Depends
from sqlmodel import SQLModel,Field,create_engine,Session,select
from typing import Annotated
from models import Hero,HeroCreate,HeroResponse,HeroResponse,Team,TeamCreate,TeamResponse,TeamUpdate
# Step 1 Hero class for Creating Table

# Step 2 Database Connection with Conn String and Function
DB_URL = "postgresql://usman.qau12:4furb3sejMRK@ep-empty-darkness-04003085.ap-southeast-1.aws.neon.tech/empty?sslmode=require"
engine =create_engine("postgresql://usman.qau12:4furb3sejMRK@ep-empty-darkness-04003085.ap-southeast-1.aws.neon.tech/empty?sslmode=require")
def create_tables():
    SQLModel.metadata.create_all(engine)

# Step 3 Object of Faste API
app = FastAPI()

# Step 3.1 Db Dependency Injection
def get_deb():
    with Session() as session:
        yield session

# Step 4 
@app.on_event("startup")
def on_startup():
    create_tables()

# Step 5 Getting Data from Table by GET Method
# @app.get("/")
# async def root():
#     return {"message":"Hello World"}
# Step 5.1 Getting All heros , getting all tables data
@app.get("/heroes",response_model=list[Hero])
def get_heroes(session:Annotated[Session,Depends(get_deb)]):
    # with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
# Step 5.3  Posting Data to table to write
# @app.post("/heroes", response_model=list[Hero])
@app.post("/heroes", response_model=HeroResponse)
# def create_hero(hero:Hero,db:Annotated[Session,Depends(get_deb)]):
def create_hero(hero:HeroCreate,db:Annotated[Session,Depends(get_deb)]):
    # with Session(engine) as session:
        db.add(hero)
        db.commit()
        db.refresh(hero)
        return hero
          

