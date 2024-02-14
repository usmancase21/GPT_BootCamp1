from fastapi import FastAPI,Depends
from sqlmodel import SQLModel,Field,create_engine,Session,select
from typing import Optional,Annotated

# Step 1 : Create Table Hero with Pydantic
# class Hero(SQLModel,table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     secret_name:str
#     age: int | None = None


# First Amendment to hanlde optional fields
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None
class HeroResponse(SQLModel):
    id: int
    name: str
    secret_name: str
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

# Step 3.1 Dependency Injection
def get_deb():
    with Session(engine) as session:
        yield session

# Step 4 Startup function
@app.on_event("startup")
def on_startup():
    create_tables()

# Step 6 Getting Data from Table by GET Method
# Step 6.1
    


@app.get("/heroes",response_model=list[Hero])
# def get_heroes():
def get_heroes(session:Annotated[Session,Depends(get_deb)]):
    # with Session(engine) as session:
    heroes = session.exec(select(Hero)).all()
    return heroes


# Step 6.3  Creating heros
# @app.post("/heroes",response_model=Hero)
# # def create_hero(hero: Hero):
# def create_hero(hero: Hero,db:Annotated[Session,Depends(get_deb)]) :
#     db.add(hero)
#     db.commit()
#     db.refresh(hero)
#     return hero

# Copy of Creating hero 
@app.post("/heroes")
def create_hero(hero: HeroCreate,db:Annotated[Session,Depends(get_deb)]) :
    print("Data fron client",hero)
    hero_to_insert=Hero.model_validate(hero)
    print("Data After Validation",hero_to_insert)
    db.add(hero_to_insert)
    db.commit()
    db.refresh(hero_to_insert)
    return hero_to_insert