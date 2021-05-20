from pydantic import BaseModel
from fastapi import Query
import enum


class Role(enum.Enum):
    ADMIN: str = "admin"
    PERSONNEL: str = "personnel"


class User(BaseModel):
    username: str
    password: str
    email: str = Query(..., regex="^([a-zA-Z0-9-.]+)@([a-zA-Z0-9-.]+).([a-zA-Z]{2,5})$")
    role: Role
