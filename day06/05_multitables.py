from fastapi import FastAPI,Depends
from sqlmodel import SQLModel,Field,create_engine,Session,select
from typing import Optional,Annotated
from fastapi import HTTPException
from fastapi import Query

# Step 1 : Create Table Hero with Pydantic
class HeroBase(SQLModel):
    name: str=Field(index=True)
    secret_name:str
    
# class Hero(SQLModel, table=True):
class Hero(HeroBase,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    age: Optional[int] = None

# class HeroCreate(SQLModel):
class HeroCreate(HeroBase):
    age: Optional[int] = None
    
# class HeroResponse(SQLModel):
class HeroResponse(HeroBase):
    id: int
    age: Optional[int] = None
    

class HeroUpdate(SQLModel):
    name: Optional[str] = Field(default=None)
    secret_name: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
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
    


@app.get("/heroes", response_model=list[Hero])
def get_heroes(session: Annotated[Session, Depends(get_deb)], offset: int = Query(default=0, le=4), limit: int = Query(default=2, le=4)):
    # heroes = session.exec(select(Hero)).all()
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@app.post("/heroes")
def create_hero(hero: HeroCreate,db:Annotated[Session,Depends(get_deb)]) :
    print("Data fron client",hero)
    hero_to_insert=Hero.model_validate(hero)
    print("Data After Validation",hero_to_insert)
    db.add(hero_to_insert)
    db.commit()
    db.refresh(hero_to_insert)
    return hero_to_insert

# Step 7

@app.get("/heroes/{hero_id}", response_model=HeroResponse)
def get_hero_by_id(hero_id: int, session: Annotated[Session, Depends(get_deb)]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
# Hero Update
@app.patch("/heroes/{hero_id}", response_model=HeroResponse)
def update_hero_by_id(hero_id: int, hero_data: HeroUpdate, session: Annotated[Session, Depends(get_deb)]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data_dict = hero_data.dict(exclude_unset=True)
    for key, value in hero_data_dict.items():
        setattr(hero, key, value)

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
# Hero Delete
@app.delete("/heroes/{hero_id}", response_model=HeroResponse)
def delete_hero_by_id(hero_id: int, session: Annotated[Session, Depends(get_deb)]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return hero