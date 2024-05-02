from flask_app import app
from flask import session, redirect, flash


@app.route("/")
def indexpage():
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")
    else:
        return redirect("/recipes")
