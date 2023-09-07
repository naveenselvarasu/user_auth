from fastapi import APIRouter, status, Depends, Security
import schemas
import models
from database import engine, Session, JWT_SECRET, JWT_ALOGORITHM
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import bcrypt
import datetime
import jwt
import datetime 

auth_route = APIRouter(prefix="/user",
                       tags=["auth"])


db = Session(bind=engine)

#-------------------JWT--------------#
def token_generation(user_id: int, business_id: int):
    expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=2, minutes=0)).isoformat()
    payload = {"user_id": user_id,
               "business_id": business_id,
               "expiry": expiry}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALOGORITHM)
    print(token)
    return token


def token_verification(token, user_id, business_id):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALOGORITHM)
            print(payload)
            print("-----------",(payload["user_id"] , int(user_id) , payload["business_id"] , int(business_id)))
            print(payload["user_id"] == int(user_id), payload["business_id"] == int(business_id) , (payload["expiry"] >= datetime.datetime.utcnow().isoformat()))

            if (payload["user_id"] == int(user_id)) and (payload["business_id"] == int(business_id)) and (payload["expiry"] >= datetime.datetime.utcnow().isoformat()):
                return payload["user_id"]
            else:
                raise HTTPException(status_code=401, detail='token expired')
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

# def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
#     return token_verification(auth.credentials)

#-------------------JWT--------------#


@auth_route.post("/signup/")
async def user_signup(request: schemas.Signup):
    hash_password = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt())
    hash_password = hash_password.decode("utf-8")
    new_user = models.User(prefix=request.prefix,
                           firstname=request.firstname,
                           lastname=request.lastname,
                           username=request.username,
                           password=hash_password,
                           mobile=request.mobile,
                           email=request.email,
                           address=request.address,
                           date_of_joining=datetime.datetime.now(),
                           is_active=request.is_active,
                           is_executive=request.is_executive)
    
    db.add(new_user)
    db.commit()
    user_obj = db.query(models.User).filter(models.User.username == request.username).first()
    user_usertype_map = models.UserUserTypeMap(user_id=user_obj.id,
                                               usertype_id=request.usertype)
    db.add(user_usertype_map)
    db.commit()
    # user_dict = {key: getattr(user_obj, key) for key in user_obj.__table__.columns.keys()}

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Sucessfully Created", headers="signup")


@auth_route.post("/signin/", status_code=status.HTTP_200_OK)
async def user_signin(request: schemas.UserSignin):
    user_obj = db.query(models.UserUserTypeMap).filter(models.UserUserTypeMap.usertype.has(business_id = request.business_id),
                                                       models.UserUserTypeMap.user.has(username = request.username)).first()
    
    if user_obj is not None:
        # user_password = b'1234'
        user_password = request.password.encode("utf-8")
        # db_password = b'$2b$12$KLyA3buoUSyqJ1TbDHNxjOkWhLHoizjyLKE84CrHCWlShKLbqfXAS'
        db_password = user_obj.user.password.encode("utf-8")

        if bcrypt.checkpw(user_password, db_password):
            if request.token == None or request.token == "":
                return {"token": token_generation(user_obj.id,  user_obj.usertype.business_id),
                        "business_id": user_obj.usertype.business_id,
                        "user_id":user_obj.user_id,
                        "prefix": user_obj.user.prefix,
                        "first_name": user_obj.user.firstname,
                        "last_name": user_obj.user.lastname,
                        "is_executive": user_obj.user.is_executive}
            else:
                test = token_verification(request.token, user_obj.id, user_obj.usertype.business_id)
                if test:
                    print("token_verified")
                    return {"token": request.token,
                            "business_id": user_obj.usertype.business_id,
                            "user_id":user_obj.user_id,
                            "prefix": user_obj.user.prefix,
                            "first_name": user_obj.user.firstname,
                            "last_name": user_obj.user.lastname,
                            "is_executive": user_obj.user.is_executive}
                       
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enter valid username or password", headers="signin")


@auth_route.get("/get/modules/")
# async def user_signup(Secret=Depends(auth_wrapper)):
async def user_signup(request: schemas.UserToken = Depends(token_verification)):

    modules = db.query(models.UserTypeModulesMap).filter(models.UserTypeModulesMap.is_active == True).all()
    data = [
    {
        "module_id": module.module.id,
        "module_name": module.module.name,
        "usertype": module.usertype.id,
        "sub_modules": [{"module_id": sub_module.sub_module.id,
                         "module_name": sub_module.sub_module.name,
                         "usertype": sub_module.usertype.id
                         } 
                         for sub_module in db.query(models.UserTypeSubModulesMap).filter(models.UserTypeSubModulesMap.is_active == True,
                                                                                         models.UserTypeSubModulesMap.sub_module.has(module_id = module.module.id)).all()]
    }
    for module in modules
]
    # data = []
    # for module in modules:
    #     module_data = {
    #         "module_id": module.module.id,
    #         "module_name": module.module.name,
    #         "usertype": module.usertype.id,
    #         "sub_module": []
    #     }
        # for submodule_map in module.usertype_modules_map:
        #     submodule = submodule_map.sub_module
        #     module_data["sub_module"].append({
        #         "module_id": submodule.id,
        #         "module_name": submodule.name,
        #         "usertype": submodule.usertype_sub_modules_map[0].usertype_id if submodule.usertype_sub_modules_map else None
        #     })
    #     data.append(module_data)
    # db.close()
    return data
