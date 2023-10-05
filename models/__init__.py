#!/usr/bin/python3
<<<<<<< HEAD
"""Instantiates a storage object.
"""
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
=======
"""This module instantiates an object of class FileStorage"""
import os

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
    storage.reload()
else:

    from models.engine.file_storage import FileStorage

    storage = FileStorage()
    storage.reload()
>>>>>>> 4522ce7d33db649bb27d03c26fe635d9c6886bb8
