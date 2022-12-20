from database.crud_imports import *


def create_users(db_session: scoped_session, db_user: models.User):
    if db_session.execute(select(models.User).where(models.User.email==db_user.email)).fetchone:
        print("DEBUG: ADD RAISE ERROR TO CREATE_USERS FUNCTION")
        return
    else:
        db_user.password = generate_password_hash(db_user.password)    
        return db_session.add(db_user)

def check_for_user(engine: Engine, user: models.User):
    with engine.connect() as conn:
        stmt = select(models.User).where(models.User.email == user.email)
        results = conn.scalars(stmt).one()
        return results
@dbcommit
def get_user_info(db_session: scoped_session, user: models.User):
    stmt = select(models.User).where(models.User.id != user.id)
    results = db_session.scalars(stmt)
    return results
    

def delete_users(engine: Engine):
    with engine.connect() as conn:
        stmt = delete(models.User)
    