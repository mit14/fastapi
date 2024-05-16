from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from .config import settings
# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgresql://mitpatel:Password123@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{settings.database_password}@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# connection to db
# while True:
#     try:
#         #conn = psycopg2.connect(host, database, user, password, column name mapping )
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='KhiaraLeo@1412', cursor_factory= RealDictCursor )
#         cursor = conn.cursor()
#         print("database connection was successful")
#         break
#     except Exception as error:
#         print("Connection to DB failed")
#         print("Error:", error)
#         time.sleep(2)