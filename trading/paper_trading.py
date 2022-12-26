from flask import Blueprint

from auth.authorisations import login_required

trading_blueprint = Blueprint("trading_blueprint", __name__,
                            template_folder="templates",
                            static_folder="static", static_url_path="assets",
                            )

@trading_blueprint.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    return "<h1>BUY</h1>"

@trading_blueprint.route("/portfolio")
@login_required
def portfolio():
    return "<h1>Portfolio</h1>"
