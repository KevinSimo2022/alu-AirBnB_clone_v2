#!/usr/bin/python3

"""Unittests for database storage"""
import pep8
import unittest
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.base import Engine

class TestDBStorage(unittest.TestCase):
    """Unittests for testing the DBStorage class."""
    STATE_NAME = "California"
    CITY_NAME = "San_Jose"
    USER_EMAIL = "poppy@holberton.com"

    @classmethod
    def setUpClass(cls):
        """DBStorage testing setup.
        Instantiate new DBStorage.
        Fill DBStorage test session with instances of all classes.
        """
        cls.storage = DBStorage()
        cls.storage.reload()
        cls.session = cls.storage._DBStorage__session

        cls.state = State(name=cls.STATE_NAME)
        cls.session.add(cls.state)

        cls.city = City(name=cls.CITY_NAME, state_id=cls.state.id)
        cls.session.add(cls.city)

        cls.user = User(email=cls.USER_EMAIL, password="betty")
        cls.session.add(cls.user)

        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        """DBStorage testing teardown.
        Delete all instantiated test classes.
        Clear DBStorage session.
        """
        cls.session.delete(cls.user)
        cls.session.delete(cls.city)
        cls.session.delete(cls.state)
        cls.session.commit()

        cls.session.close()
        del cls.state
        del cls.city
        del cls.user
        del cls.storage

    def test_pep8_style(self):
        """Test code style with PEP 8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(
            result.total_errors, 0,
            "PEP 8 style issues found in db_storage.py")

    # ... (other test methods)

if __name__ == "__main__":
    unittest.main()

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_attributes(self):
        """Check for attributes."""
        self.assertTrue(isinstance(self.storage._DBStorage__engine, Engine))
        self.assertTrue(isinstance(self.storage._DBStorage__session, Session))

    def test_methods(self):
        """Check for methods."""
        self.assertTrue(hasattr(DBStorage, "__init__"))
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.storage, DBStorage))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_all(self):
        """Test default all method."""
        obj = self.storage.all()
        self.assertEqual(type(obj), dict)
        self.assertEqual(len(obj), 6)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_all_cls(self):
        """Test all method with specified cls."""
        obj = self.storage.all(State)
        self.assertEqual(type(obj), dict)
        self.assertEqual(len(obj), 1)
        self.assertEqual(self.state, list(obj.values())[0])

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_new(self):
        """Test new method."""
        st = State(name="Washington")
        self.storage.new(st)
        store = list(self.storage._DBStorage__session.new)
        self.assertIn(st, store)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save(self):
        """Test save method."""
        st = State(name="Virginia")
        self.storage._DBStorage__session.add(st)
        self.storage.save()
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM states WHERE BINARY name = 'Virginia'")
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(st.id, query[0][0])
        cursor.close()

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_delete(self):
        """Test delete method."""
        st = State(name="New_York")
        self.storage._DBStorage__session.add(st)
        self.storage._DBStorage__session.commit()
        self.storage.delete(st)
        self.assertIn(st, list(self.storage._DBStorage__session.deleted))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_delete_none(self):
        """Test delete method with None."""
        try:
            self.storage.delete(None)
        except Exception:
            self.fail

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_reload(self):
        """Test reload method."""
        og_session = self.storage._DBStorage__session
        self.storage.reload()
        self.assertIsInstance(self.storage._DBStorage__session, Session)
        self.assertNotEqual(og_session, self.storage._DBStorage__session)
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session = og_session


if __name__ == "__main__":
    unittest.main()