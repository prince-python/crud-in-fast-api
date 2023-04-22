from fastapi import FastAPI
from app import router as UsersRoute
from app import api as UsersApi
from tortoise.contrib.fastapi import register_tortoise
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


app = FastAPI()
app.include_router(UsersRoute.router)
app.include_router(UsersApi.app, tags=["api"])

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

try:
    register_tortoise(
        app,
        db_url="postgres://postgres:root@127.0.0.1/test",
        modules={'models': ['app.models']},
        generate_schemas=True,
        add_exception_handlers=True
    )
except:
    print("data base error")



