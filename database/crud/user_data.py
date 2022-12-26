from database.crud_imports import *

def create_users(db_session: scoped_session, db_user: models.User):
    # Check if user exists and raise error if not
    if db_session.execute(select(models.User).where(models.User.email==db_user.email)).fetchone():
        raise ExistingUserError
    else:
        db_user.password = generate_password_hash(db_user.password)    
        return db_session.add(db_user)

def get_user_info(db_session: scoped_session, user: models.User):
    stmt = select(models.User).where(models.User.email == user.email)
    results = db_session.scalar(stmt)
    return results
    
    
def check_for_user(db_session: scoped_session, user: models.User):
        """Checks if there is a matching user in database through checking email and password, if there's a match, returns the user from database"""
        
        stmt = select(models.User).where(models.User.email == user.email)
        db_user = db_session.scalar(stmt)
        if not db_user:
            raise MatchingInfoError
        if not check_password_hash(db_user.password, user.password):
            raise MatchingInfoError
        
        return db_user

def delete_users(engine: Engine):
    with engine.connect() as conn:
        stmt = delete(models.User)
        
        

class ExistingUserError(Exception):
        def __str__(self) -> str:
            return "A user with the same email already exists"
        
class MatchingInfoError(Exception):
    def __str__(self) -> str:
         return "Email or password are incorrect"