from fastapi import FastAPI
from auth_routes import auth_route
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Session
import models

from sqlalchemy.orm import joinedload

app = FastAPI(title="My API")

origins = ["http://localhost:8000"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
                   allow_headers=[],)

app.include_router(auth_route)


Base.metadata.create_all(bind=engine)
db = Session(bind=engine)




