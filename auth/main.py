from fastapi import FastAPI
from auth_routes import auth_route
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Session
import models

from sqlalchemy.orm import joinedload

app = FastAPI(title="My API")

origins = ["http://ea.com"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=False,
                   allow_methods=["GET", "POST", "PUT", "DELETE"],
                   allow_headers=[],)

app.include_router(auth_route)


Base.metadata.create_all(bind=engine)
db = Session(bind=engine)
@app.get("/get/modules/")
async def user_signup():
    return db.query(models.UserTypeSubModulesMap).filter(models.UserTypeSubModulesMap.is_active == True).options(joinedload(models.UserTypeSubModulesMap.sub_module)).all()




