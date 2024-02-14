from typing import Optional 
from sqlmodel import Field, SQLModel, create_engine

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


# Step 4 Calling main function
if __name__ == "__main__":
    create_db_and_table()