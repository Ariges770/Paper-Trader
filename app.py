import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from public_pages.public_pages import public_pages_blueprint
from auth.authorisations import auth_blueprint
from trading.paper_trading import trading_blueprint
from database.database import Base
from database.database import engine


app = Flask(__name__)

app.register_blueprint(public_pages_blueprint, url_prefix="/")
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(trading_blueprint, url_prefix="/trading")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


app.config["SESSION_PERMANENT"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = engine.url
app.config["SESSION_TYPE"] = "sqlalchemy"

db = SQLAlchemy(app, 
                engine_options={"pool_pre_ping":True, "pool_recycle":60, "echo_pool":False,
                                        "pool_size":5, "pool_timeout":30}
                )
app.config["SESSION_SQLALCHEMY"] = db
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=15)
# The use of Session(app) somehow deletes session data on redirect, https://stackoverflow.com/questions/61972873/flask-session-lost-data
app.secret_key = "KEdDmjhr87432gpg7G&Ffg979TfiUQ"

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

print("DEBUG: ", app.url_map)

# with app.app_context():
#     db.create_all()

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

if __name__=="__main__":
    app.run(load_dotenv=True)