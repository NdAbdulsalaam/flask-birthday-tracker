import os

# from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from flask_sqlalchemy import SQLAlchemy
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# ensure database sqlite 
app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthdays.db'
# Configure CS50 Library to use SQLite database
db = SQLAlchemy(app)
# db = SQL("sqlite:///birthdays.db")

# # ------------------------------------------
# # Import Models
# #----------------------------------------------

from models import Birthdays


# ------------------------------------------
# Routes
#----------------------------------------------

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        
        # Add to database
        new_friend_date = Birthdays(name=name, month=month, day=day)
        db.session.add(new_friend_date)
        db.session.commit()
        return redirect("/")
# Add user to the database
    else:
        # TODO: Display the entries in the database on index.html
        birthdays = Birthdays.query.all()
        return render_template("index.html", birthdays=birthdays)

# Endpoint for deleting a record
@app.route("/delete/<id>", methods = ['GET', 'POST'])
def delete(id):
    my_data = Birthdays.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('index'))