
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "OK"}

# Database connection
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://fastapi:QWERTYY12345!@fastapi-db/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for the ORM models
Base = declarative_base()

# Example ORM model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# API endpoint to create a user
@app.post("/users/")
def create_user(name: str, email: str):
    try:
        db = SessionLocal()
        user = User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        return {"error": str(e)}
    finally:
        db.close()
        
# API endpoint to get all users
@app.get("/users/")
def get_users():
    try:
        db = SessionLocal()
        users = db.query(User).all()
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        db.close()        