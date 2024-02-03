from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated,Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel



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
#  when table is not true its pydantic model
# class Location(SQLModel):
#     name: str = Field(index=True, primary_key=True)
#     location: str
class Location(SQLModel, table=True):
    name: str = Field(index=True, primary_key=True)
    location: str

# locations = {
#     "zia": Location(name="Zia", location="Karachi"),
#     "ali": Location(name="Ali", location="Lahore"),
#     "usman":Location(name="Usman", location="Islamabad"),
#     "kamran":Location(name="Kamran", location="Rawalpindi"),
# }


database_url = "postgresql://usman.qau12:4furb3sejMRK@ep-empty-darkness-04003085.ap-southeast-1.aws.neon.tech/hero_class?sslmode=require"


engine = create_engine(database_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    

# posting data to database 
@app.post("/person/")
def create_person(person_data: Location):
    with Session(engine) as session:
        session.add(person_data)
        session.commit()
        session.refresh(person_data)
        return person_data




    
# getting back data from database
@app.get("/person/")
def read_all_persons():
    with Session(engine) as session:
        loc_data = session.exec(select(Location)).all()
        return loc_data

# depency function
def get_location_or_404(name:str)->Location:
    with Session(engine) as session:
        loc_data = session.exec(select(Location).where(Location.name == name)).first()
        if not loc_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No location found for {name}")
        return loc_data

@app.get("/location/{name}")
# @app.get("/location/{asd}")
def get_person_location(name:str, location: Annotated[Location, Depends(get_location_or_404)]):
    return location