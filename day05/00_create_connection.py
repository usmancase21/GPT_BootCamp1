from dotenv import load_dotenv, find_dotenv

from os import getenv
from typing import Optional

from sqlmodel import Field,SQLModel,create_engine

_:bool = load_dotenv(find_dotenv())

# postges_url = getenv("POSTGRESS_URL")
# print(postges_url)  # Add this line to check the value of POSTGRESS_URL
# engine = create_engine(postges_url,echo=True)
engine = create_engine('postgresql://usman.qau12:4furb3sejMRK@ep-empty-darkness-04003085.ap-southeast-1.aws.neon.tech/sqlmodel1?sslmode=require', echo=True)

class Team(SQLModel,table=True):

    id:Optional[int] = Field(primary_key=True)
    name:str 
    headquarter:str

class Hero(SQLModel,table=True):
    """
    create a hero table with
    columns:id,name,secret_name,age,and team_id
    foreign key:team_id references id in Team table
    """
    id:Optional[int] = Field(primary_key=True)
    name:str=Field(index=True)
    secret_name:str
    age:Optional[int] = Field(default=None,index=True)
    team_id:Optional[int] = Field(default=None,foreign_key="team.id")

# # create a databpostges_url = getenv("POSTGRESS_URL")
# print(postges_url)  # Add this line to check the value of POSTGRESS_URL
# # engine = create_engine(postges_url,echo=True)ase engine using create_engine
# # postges_url = getenv("POSTGRESS_URL")
# # engine = create_engine(postges_url,echo=True)




def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():
    create_db_and_tables()

if __name__ == "__main__":
    main()




   