from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from decouple import config



# JWT 
JWT_SECRET = config("secret")
JWT_ALOGORITHM = config("algorithm")

    


# psycopg2 (dialect+driver://username:password@host:port/database)

url_object = URL.create(
    "postgresql+psycopg2",
    username=config("DB_USER"),
    password=config("DB_PASSWORD"),  
    host=config("DB_HOST"),
    database=config("DB_NAME"),
)
# url_object = "postgresql+psycopg2://user_auth:user_auth@localhost/user_auth"
engine = create_engine(url_object)
# engine = create_engine("postgresql+psycopg2://user_auth:user_auth@localhost/user_auth")
Base = declarative_base()

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

