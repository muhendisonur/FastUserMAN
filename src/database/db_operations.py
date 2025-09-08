from sqlalchemy import create_engine
from config import db_path
from database.models import Base

def init_models() -> None:
    """ This func creates all the models from models.py as tables in the database. """
    engine = create_engine(f"sqlite:///{db_path}", echo=True)
    Base.metadata.create_all(engine) # creates all models which are under models.py file on Db
