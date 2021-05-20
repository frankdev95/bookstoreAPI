from fastapi import FastAPI, Body, Header, File
from routes.v1 import app_v1
from passlib.context import CryptContext

app = FastAPI()


app.mount("/v1", app_v1)

