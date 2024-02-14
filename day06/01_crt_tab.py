from fastapi import FastAPI,Depends
from sqlmodel import SQLModel,Field,create_engine,Session,select
from typing import Optional

# Step 1 : Create Table Hero with Pydantic
class Hero(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name:str
    age: Optional[int] = None

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

# Step 5 Getting Data from Table by GET Method
@app.get("/")
async def root():
    return {"message":"Hello World"}