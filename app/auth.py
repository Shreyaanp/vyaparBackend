from fastapi import HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from app.database import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserInDB(User):
    hashed_password: str

async def register_user(user: User):
    user_in_db = db.users.find_one({"email": user.email})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    new_user = UserInDB(**user.dict(), hashed_password=hashed_password)
    db.users.insert_one(new_user.dict())
    return {"message": "User registered successfully"}

async def login_user(email: str, password: str):
    user_in_db = db.users.find_one({"email": email})
    if not user_in_db or not pwd_context.verify(password, user_in_db["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    user_details = {
        "id": str(user_in_db["_id"]),
        "first_name": user_in_db["first_name"],
        "last_name": user_in_db["last_name"],
        "email": user_in_db["email"],
        "password": user_in_db["password"],
        "hashed_password": user_in_db["hashed_password"]
    }

    return user_details
