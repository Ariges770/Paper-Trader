from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from public_pages.public_pages import public_pages_blueprint

from database.database import Base
from database.database import engine


app = Flask(__name__)

Base.metadata.create_all(bind=engine)

app.register_blueprint(public_pages_blueprint, url_prefix="/")


# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_PERMANENT"] = True
# app.config["SQLALCHEMY_DATABASE_URI"] = CONST_URL
# app.config["SESSION_TYPE"] = "sqlalchemy"

# db = SQLAlchemy(app)
# app.config["SESSION_SQLALCHEMY"] = db
# app.config['PERMANENT_SESSION'] = True
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=15)
# Session(app)

# # with app.app_context():
# #     db.create_all()

if __name__=="__main__":
    Base.metadata.create_all(bind=engine)
    app.run(load_dotenv=True)