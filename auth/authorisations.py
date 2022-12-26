from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from typing import Any
from functools import wraps

from database.crud import user_data, transactions
from database.models import models
from database.crud_imports import dbconnect, scoped_session, Session

auth_blueprint = Blueprint("auth_blueprint", __name__,
                            template_folder="templates",
                            static_folder="static", static_url_path="assets",
                            )

@auth_blueprint.route("/login", methods = ["POST"])
@dbconnect
def index(db_session: scoped_session[Session]):
    print(request.form)
    login_email = request.form.get("login_email")
    login_password = request.form.get("login_password")
    if login_email != None and login_password != None:
        user = models.User(email=login_email, password=login_password)
        # user_data.get_user_info(db_session, user=db_user)
        session["login_statement"] = None
        # Ensure login email and password match a database entry
        try:
            session["user_id"] = user_data.check_for_user(db_session, user=user).id
        except user_data.MatchingInfoError:
            session["login_statement"] = "Email or password are incorrect"
        return redirect(url_for("trading_blueprint.portfolio"))
    
    else:
        session["login_statement"] = "Incomplete login details."
        return redirect(url_for("public_pages_blueprint.index"))
    
    
    
@auth_blueprint.route("/register", methods = ["POST"])
@dbconnect
def register(db_session: scoped_session[Session]):
    
    register_email = request.form.get("register_email")
    verify_email = request.form.get("verify_email")
    register_password = request.form.get("register_password")
    verify_password = request.form.get("verify_password")
    
    form_inputs = [register_email, verify_email, register_password, verify_password]
    
    # Ensure all input box's are completed
    if None in form_inputs:
        session["register_statement"] = "Missing registration user input."
        return redirect(url_for("public_pages_blueprint.index"))
    else:
        register_email = str(register_email)
        register_password = str(register_password)
          
    # Ensure emails and passwords match
    if register_email != verify_email:
        session["register_statement"] = "Emails don't match."
        return redirect(url_for("public_pages_blueprint.index"))
    if register_password != verify_password:
        session["register_statement"] = "Passwords don't match."
        return redirect(url_for("public_pages_blueprint.index"))
    
    db_user = models.User(email=register_email, password=register_password)
    
    # Adjust statement by registration box based on if an account was successfully made or not
    try:
        user_data.create_users(db_session, db_user)
        session["register_statement"] = None
    except user_data.ExistingUserError:
        session["register_statement"] = "A user with the same email already exists"
        
    return redirect(url_for("public_pages_blueprint.index"))


def login_required(func):
    
    @wraps(func)
    def decorated_login_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("public_pages_blueprint.index"))
        return func(*args, **kwargs)
    return decorated_login_function