from pydantic import EmailStr, BaseModel as Schema
from typing import Optional
import datetime
import models


class Business(Schema):
    name: str




class UserType(Schema):
    business_id: int
    name: str


class UserUserTypeMap(Schema):
    user_id: int
    user_type_id: int


# class Module(Schema):
#     business_id: int
#     name: str


# class SubModule(Schema):
#     module_id: int
#     name: int


# class UserTypeModulesMap(Schema):
#     user_type_id: int
#     module_id: int
#     is_active: bool


# class UserTypeSubModulesMap(Schema):
#     user_type_id: int
#     sub_module_id: int
#     is_active: bool
    

class UserSignin(Schema):
    business_id: int
    username: str
    password: str
    token: str = None


class Signup(Schema):
    prefix: str
    firstname: str
    lastname: str
    username: str
    password: str
    mobile: str
    email: EmailStr
    address: Optional[str]
    # date_of_joining: Optional[datetime.datetime]
    is_active: Optional[bool]
    is_executive: Optional[bool]
    usertype: int


class User(Schema):
    prefix: str
    firstname: str
    lastname: str
    username: str

class UserToken(Schema):
    token: str = None
    user_id: int
    business_id: int
