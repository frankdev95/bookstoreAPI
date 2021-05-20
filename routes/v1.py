from fastapi import FastAPI, Body, Header, File, Depends, Form, HTTPException
from models.author import Author
from models.user import User
from models.book import Book
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from util.security import authenticate_user, create_jwt_token
from models.jwt_user import JWTUser
from typing import Optional

app_v1 = FastAPI(openapi_prefix="/v1")


@app_v1.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header("custom-header")):
    return {"user": user}


@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie", value="cookie-api")
    return {"file size": len(profile_photo)}


@app_v1.get("/user", response_model=User, response_model_include={"username", "email", "role"})
async def get_user_validation(password: str = "123"):
    user = {
        "username": "bookworm123",
        "password": "somehashedpw",
        "email": "booklover123@gmail.com",
        "role": "personnel"
    }
    return User(**user)


@app_v1.get("/book/{isbn}", response_model=Book)
async def get_book_from_isbn(isbn: int):
    return {"isb": isbn}


@app_v1.get("/author/{id}/book")
async def get_authors_books(id: int, category: str = "thriller", order: str = "asc"):
    return {"id": id, "category": category, "order": order}


@app_v1.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}


@app_v1.post("/user/author")
async def post_author_user(user: User, author: Author, bookstore: str = Body(..., embed=True)):
    return {"user": user, "author": author, "bookstore": bookstore}


@app_v1.post("/token")
async def get_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = JWTUser(**{
        "username": form_data.username,
        "password": form_data.password,
        "disabled": False,
        "role": "admin"
    })

    if authenticate_user(user) is not None:
        response.headers['Authorization'] = f"Bearer {create_jwt_token(user)}"
        return {"Message": "Authorization Successful"}
    else:
        raise HTTPException(HTTP_401_UNAUTHORIZED)


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app_v1.get("/items")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons