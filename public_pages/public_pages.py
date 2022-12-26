from datetime import datetime
from decimal import Decimal
from flask import Blueprint, render_template, url_for, redirect, session, request
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

    return render_template("index.html")
