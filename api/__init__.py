import logging
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

# database setup
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

logger = logging.getLogger(__name__)
