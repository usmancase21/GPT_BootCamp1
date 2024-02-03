from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated,Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel


# Step 1 Object of FastAPI

app = FastAPI(
    title="Location Finder API", 
    version="1.0.0", 
    servers=[
            {
                "url": "https://fox-informed-maggot.ngrok-free.app",
                "description": "Production Server"
            },
            {
                "url": "http://localhost:8000",
                "description": "Development Server"
            }
        ]
)

#  Step 2 With SQL Model and Pydantic and Non Data Base

class Location(SQLModel):
    name: str = Field(index=True, primary_key=True)
    location: str

# Step 2.1 Pydantic Step Hard Coded Value with non Database
#     locations = {
#     "zia": Location(name="Zia", location="Karachi"),
#     "ali": Location(name="Ali", location="Lahore"),
#     "usman":Location(name="Usman", location="Islamabad"),
#     "kamran":Location(name="Kamran", location="Rawalpindi"),
# }

# Step 3 Database Step non Pydantic Creating and Connecting Database with DB Engine
# with personsdb
database_url = "postgresql://usman.qau12:4furb3sejMRK@ep-empty-darkness-04003085.ap-southeast-1.aws.neon.tech/hero_class?sslmode=require"
engine = create_engine(database_url)


# Step 4 handling Location Error /location/error
# def get_location_or_404(name:str)->Location:
#     loc = locations.get(name.lower())
#     if not loc:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No location found for {name}")
#     return loc
# Step 4.1 Creating database insertin functioin
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
# Step 5 for location/{name} any name
# @app.get("/location/{name}")
# @app.get("/location/{asd}")
# step 5.1 Posting Data to database using Post Method
@app.post("/person/")
def create_person(person_data: Location):
    with Session(engine) as session:
        session.add(person_data)
        session.commit()
        session.refresh(person_data)
        return person_data
# Step 6 getting data from person simple
# def get_person_location(name:str, location: Annotated[Location, Depends(get_location_or_404)]):
#     return location
# Step 6.1 getting data from person 
# getting back data from database with /person from get /person method
# Step 6.2 
# depency function handling post error for custom gpt
def get_location_or_404(name:str)->Location:
    with Session(engine) as session:
        loc_data = session.exec(select(Location).where(Location.name == name)).first()
        if not loc_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No location found for {name}")
        return loc_data
# Step 6.3 getting data for custom gpt for only single person
@app.get("/person/")
def read_heroes():
    with Session(engine) as session:
        loc_data = session.exec(select(Location)).all()
        return loc_data
# Step 6.4 getting data with persona and its location
@app.get("/location/{name}")
# @app.get("/location/{asd}")
def get_person_location(name:str, location: Annotated[Location, Depends(get_location_or_404)]):
    return location