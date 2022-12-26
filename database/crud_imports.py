from sqlalchemy import select, insert, update, delete
from sqlalchemy import Select, Insert, Update, Delete, Engine
from sqlalchemy.orm import Session, scoped_session
# from sqlalchemy.orm import Session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from decimal import Decimal
from typing import Union, Any
from functools import wraps

from database.database import engine, sessionmaker
from database.models import models 
from database.database import db_SessionLocal, db_SessionLoc


def dbconnect(func):
    
    @wraps(func)
    def inner(*args, **kwargs):
        kwargs["db_session"] = db_SessionLoc  # with all the requirements
        try:
            return func(*args, **kwargs)
        except:
            kwargs["db_session"].rollback()
            raise
        finally:
            kwargs["db_session"].commit()
            kwargs["db_session"].remove()
    # inner.__name__ = func.__name__
    return inner

def dbcommit(func):
    
    @wraps(func)
    def commit(*args, **kwargs):
        # Ensure first arg is session object, else, return function
        if type(args[0]) != scoped_session:
            return func(*args, **kwargs)
        
        db_session = args[0]
        try:
            return func(*args, **kwargs)
        except:
            db_session.rollback()
            raise
        finally:
            db_session.commit()
            
    # commit.__name__ = func.__name__
    return commit