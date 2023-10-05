#!/usr/bin/python3
"""Defines the DBStorage engine."""
import datetime
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """Represents a database storage engine.
    Attributes:
	@@ -35,25 +34,24 @@ def __init__(self):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects of the given class.
        If cls is None, queries all types of objects.
        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            classes = [State, City, User, Place, Review, Amenity]
        elif isinstance(cls, str):
            classes = [eval(cls)]
        else:
            classes = [cls]

        objs = []
        for cls in classes:
            objs.extend(self.__session.query(cls).all())

        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}


    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)