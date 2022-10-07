# import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# if os.environ.get("PYTHON_ENVIRONMENT") == 'production':
#     SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
#     engine = create_engine(
#         SQLALCHEMY_DATABASE_URL, 
#     )
# else:
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

