from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_objs import CountryTable, BorderTable, MapTable



class DbHelper():
    @classmethod
    def __init__(cls):
        cls.engine = create_engine('mysql://dgray:@localhost/maps')
        cls.session_generator = sessionmaker(bind=cls.engine)
        cls.base = declarative_base()
        cls.base.metadata.create_all(cls.engine)
        cls.session = cls.session_generator()
    
    @classmethod
    def create_country(cls, country):
        country_obj = CountryTable(
            country.x,
            country.y,
            -1,
            [],
            []
        )
        cls.session.add(country_obj)
        cls.session.commit()

    @classmethod
    def create_border(cls, border):
        border_obj = CountryTable(
            border.intercept,
            border.slope,
            
        )
        cls.session.add(country_obj)
        cls.session.commit()