from flask import Blueprint, session, redirect, url_for, flash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    name = session.get("name", "")
    session.clear()
    flash(f"Goodbye, {name}! You have been logged out.", "info")
    return redirect(url_for("login"))
