from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.context import CryptContext
from .models import *
import typing
from fastapi_login import LoginManager


router = APIRouter()
SECRET = 'your-secret-key'
manager = LoginManager(SECRET, token_url='/auth/token')


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


@router.get("/login/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
    })


@manager.user_loader()
async def load_user(email: str):
    user = await User.get(email=email)
    return user


@router.post('/loginuser/', response_class=HTMLResponse)
async def login(request: Request, Email: str = Form(...), Password: str = Form(...)):
    user = await User.get(email=email)

    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    if email != user.email:
        return RedirectResponse('/login/', status_code=status.HTTP_302_FOUND)
    elif verify_password(Password, user.password):
        return RedirectResponse('/login/', status_code=status.HTTP_302_FOUND)
    else:
        persons = await User.all()
        return templates.TemplateResponse("table.html", {
            "request": request,
            "persons": persons
        })


@router.post("/delete/", response_class=HTMLResponse)
async def delete(request: Request, id: int = Form(...)):
    pk = int(id)
    user_obj = await User.get(id=pk).delete()
    persons = await User.all()
    return templates.TemplateResponse("table.html", {
        "request": request,
        "persons": persons
    })


@router.get("/login/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("update.html", {
        "request": request,
        "persons": persons
    })


@router.get("/update/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):
    person = await User.get(id=id)
    return templates.TemplateResponse("update.html", {
        "request": request,
        "person": person
    })


@router.post("/update_detials/")
async def update_detials(request: Request, id: int= Form(...),
                 Name: str = Form(...),
                 Email: str = Form(...),
                 Phone: str = Form(...),
                 ):
    person = await User.get(id=id)
    await person.filter(id=id).update(email=Email,
                                      name=Name,
                                      phone=Phone
                                      )
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)
