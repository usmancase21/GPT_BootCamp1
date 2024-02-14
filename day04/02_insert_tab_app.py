from typing import Optional 
from sqlmodel import Field, SQLModel, create_engine,select
from sqlalchemy.orm import Session

# Step 1 - Define the model with Hero class to create simple table
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

# Step 2 - Create the database engine and connection string
    
database_connection_str ="postgresql://usman.qau12:4furb3sejMRK@ep-empty-darkness-04003085.ap-southeast-1.aws.neon.tech/Class04?sslmode=require"
engine = create_engine(database_connection_str,echo=True)

# Step 3 create Table in function
def create_db_and_table():
    SQLModel.metadata.create_all(engine)

# Step 4 Inserting Data into table
def create_hero():
    """
    Inserts data into the database.

    This function creates instances of the Hero class and adds them to the session.
    It then commits the changes to the database and closes the session.

    """
    hero_1 = Hero(name="Usman Awan",secret_name="HOD",age=20)
    hero_2 = Hero(name="Kamran Abbas",secret_name="PC",age=30)
    hero_3 = Hero(name="Zain",secret_name="Student",age=25)
    session = Session(engine)
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()
    session.close()
# Step 4.1 selecting data from database
def get_hero():
    session = Session(engine)
    # statement = select(Hero).where(Hero.name=="Kamran Abbas")
    statement = select(Hero).where(Hero.id==4)
    # statement = select(Hero).offset(4).limit(2)
    result = session.exec(statement)
    print(result.all())
    # print(result.one())
    # for hero in result:
    #     print("print invividual")
    #     print(hero.name)
# Step 4.2 Update Table
def update_hero():
    session = Session(engine)
    statement = select(Hero).where(Hero.name=="musa")
    result = session.exec(statement).first()
    print(result)
    result.age=24
    session.add(result)
    session.commit()
    print("Updated Data")
    print(result)
    session.close()
# step 4.3 Delete Data from Table
def delte_hero():
    session = Session(engine)
    statement = select(Hero).where(Hero.id==4)
    result = session.exec(statement).first()
    print(result)
    session.delete(result)
    session.commit()
    session.close()

# Step 5 Calling main function and all other classes
if __name__ == "__main__":
    # create_db_and_table()
    # create_hero()
    # get_hero()
    # update_hero()
    delte_hero()
