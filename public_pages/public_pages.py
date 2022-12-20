from datetime import datetime
from decimal import Decimal
from flask import Blueprint, render_template, url_for, redirect
from typing import Any

import time

from database.crud import user_data, transactions
from database.models import models
from database.crud_imports import dbconnect, scoped_session, Session

public_pages_blueprint = Blueprint("public_pages_blueprint", __name__,
                                   template_folder="templates",
                                   static_folder="static", static_url_path="assets")

@public_pages_blueprint.route("/")
@dbconnect
def index(db_session: scoped_session[Session]):
    db_user = models.User(email="nextafter@gmail.com", password="test")
    user_data.create_users(db_session, db_user)
    
    # db_transaction = Transaction(
    #     date=datetime.now(), transaction_type="buy", ticker="BABA", 
    #     shares=4, share_price=90, cash_balance=(10000-(4*90)), person_id=2
    #     )
    
    # transaction = transactions.make_transaction(session, db_transaction)
    
    for user in user_data.get_user_info(db_session, db_user):
        print(user)
            
    return render_template("index.html")



@public_pages_blueprint.route("/sleep/<int:time_length>")
def sleep(time_length):
    for seconds in range(time_length):
        print(seconds * 1, "seconds")
        time.sleep(1)
    return redirect(url_for("public_pages_blueprint.index"))