from fastapi import FastAPI,Depends
from sqlmodel import SQLModel,Field,create_engine,Session,select
from typing import Optional,Annotated
from fastapi import Query
from sqlmodel import Field, Relationship


class TeamBase(SQLModel):
    name:str
    headquarters:str

class Team(TeamBase, table=True):
    id: int = Field(default=None, primary_key=True)
    heroes:list["Hero"]=Relationship(back_populates="team")
class TeamCreate(TeamBase):
    name: str
    headquarter: str
class TeamResponse(TeamBase):
    id: int
class TeamUpdate(SQLModel):
    name: Optional[str] = Field(default=None)
    age: int | None = None
class HeroBase(SQLModel):
    name: str=Field(index=True)
    secret_name:str
    
# class Hero(SQLModel, table=True):
class Hero(HeroBase,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    age: Optional[int] = None
    team_id:int = Field(default=None, foreign_key="team.id")
    team:Team =Relationship(back_populates="heroes")

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
