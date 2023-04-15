from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.context import CryptContext
from .models import *
import typing

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# def flash(request: Request, message: typing.Any, category: str = "") -> None:
#     if "_messages" not in request.session:
#         request.session["_messages"] = []
#         request.session["_messages"].append(
#             {"message": message, "category": category})


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, })


@router.post("/ragistration/", response_class=HTMLResponse)
async def read_item(request: Request, full_name: str = Form(...),
                    Email: str = Form(...),
                    Phone: str = Form(...),
                    Password: str = Form(...)):

    if await User.filter(email=Email).exists():
        # flash(request, "email already register")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    elif await User.filter(phone=Phone).exists():
        # flash(request, "phone number already register")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    else:
        user_obj = await User.create(email=Email, name=full_name, phone=Phone, password=get_password_hash(Password))
        # flash(request, "user sucessfully registered")
        return templates.TemplateResponse("login.html", {"request": request, })



@router.get("/table/", response_class=HTMLResponse)
async def read_item(request: Request):
    persons = await User.all()
    return templates.TemplateResponse("table.html", {
        "request": request,
        "persons": persons
    })