from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, foreign
# from sqlalchemy_utils.types import ChoiceType
from datetime import datetime


class Business(Base):
    __tablename__ = "business"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    usertype = relationship("UserType", back_populates="business")
    module = relationship("Module", back_populates="business")

    def __repr__(self):
        return f"<Business {self.name}"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    prefix = Column(String(5))
    firstname = Column(String(30))
    lastname = Column(String(30))
    username = Column(String, unique=True)
    password = Column(Text)
    mobile = Column(String(13))
    email = Column(String, unique=True)
    address = Column(Text, nullable=True)
    date_of_joining = Column(DateTime(timezone=True), default=datetime.utcnow)
    is_active = Column(Boolean, nullable=True, default=True)
    is_executive = Column(Boolean, nullable=True, default=False)

    user_usertype_map = relationship("UserUserTypeMap", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}"


class UserType(Base):
    __tablename__ = "usertype"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("business.id"))
    name = Column(String(40))

    business = relationship("Business", back_populates="usertype")
    user_usertype_map = relationship("UserUserTypeMap", back_populates="usertype")
    usertype_modules_map = relationship("UserTypeModulesMap", back_populates="usertype")
    usertype_sub_modules_map = relationship("UserTypeSubModulesMap", back_populates="usertype")

    def __repr__(self):
        return f"<UserType {self.name}"


class UserUserTypeMap(Base):
    __tablename__ = "user_usertype_map"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    usertype_id = Column(Integer, ForeignKey("usertype.id"))
    token = Column(Text, nullable=True)

    user = relationship("User", back_populates="user_usertype_map")
    usertype = relationship("UserType", back_populates="user_usertype_map")

    def __repr__(self):
        return f"<UserUserTypeMap {self.user.firstname, self.user.lastname, self.user.id}"


class Module(Base):
    __tablename__ = "module"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("business.id"))
    name = Column(String(100))
    link = Column(String(200), nullable=True)
    icon_name = Column(String(150), nullable=True)


    business = relationship("Business", back_populates="module")
    sub_module = relationship("SubModule", back_populates="module")
    usertype_modules_map = relationship("UserTypeModulesMap", back_populates="module")


class SubModule(Base):
    __tablename__ = "sub_module"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("module.id"))
    name = Column(String(100))
    link = Column(String(200), nullable=True)
    icon_name = Column(String(150), nullable=True)

    module = relationship("Module", back_populates="sub_module")
    usertype_sub_modules_map = relationship("UserTypeSubModulesMap", back_populates="sub_module")


class UserTypeModulesMap(Base):
    __tablename__ = "usertype_modules_map"
    id = Column(Integer, primary_key=True)
    usertype_id = Column(Integer, ForeignKey("usertype.id"))
    module_id = Column(Integer, ForeignKey("module.id"))
    is_active = Column(Boolean, default=True)

    usertype = relationship("UserType", back_populates="usertype_modules_map")
    module = relationship("Module", back_populates="usertype_modules_map")


class UserTypeSubModulesMap(Base):
    __tablename__ = "usertype_sub_modules_map"
    id = Column(Integer, primary_key=True)
    usertype_id = Column(Integer, ForeignKey("usertype.id"))
    sub_module_id = Column(Integer, ForeignKey("sub_module.id"))
    is_active = Column(Boolean, default=True)

    usertype = relationship("UserType", back_populates="usertype_sub_modules_map")
    sub_module = relationship("SubModule", back_populates="usertype_sub_modules_map")
