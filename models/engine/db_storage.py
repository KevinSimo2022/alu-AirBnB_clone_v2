import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Represents database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize object"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')

        self.__engine = sqlalchemy.create_engine(
            'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
                user, password, host, database),
            pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Gets all objects depending on the class name"""
        classes = {
            'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        obj_dict = {}

        with self.__session() as session:
            if cls is not None and cls in classes:
                class_objects = session.query(classes[cls]).all()
                for obj in class_objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    obj_dict[key] = obj

            if cls is None:
                for cls in classes:
                    class_objects = session.query(classes[cls]).all()
                    for obj in class_objects:
                        key = f"{obj.__class__.__name__}.{obj.id}"
                        obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """Adds the object to the current database session"""
        with self.__session() as session:
            session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        with self.__session() as session:
            session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session obj if not None"""
        with self.__session() as session:
            if obj is not None:
                session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the session"""
        self.__session.remove()
