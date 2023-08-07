from sqlalchemy import Integer, Column, String, ARRAY
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker


DSN = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres'
engine = create_async_engine(DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession,
                       expire_on_commit=False)
Base = declarative_base()


class SwapiPeople(Base):
    __tablename__ = 'swapi_people'
    id = Column(Integer, primary_key=True)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(ARRAY(String))
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(ARRAY(String))
    starships = Column(ARRAY(String))
    vehicles = Column(ARRAY(String))
