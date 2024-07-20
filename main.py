from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

##Connect to Database
conn = sqlite3.connect('cafes.db')
cursor = conn.cursor()


# ##Cafe TABLE Configuration
# class Cafe(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), unique=True, nullable=False)
#     map_url = db.Column(db.String(500), nullable=False)
#     img_url = db.Column(db.String(500), nullable=False)
#     location = db.Column(db.String(250), nullable=False)
#     seats = db.Column(db.String(250), nullable=False)
#     has_toilet = db.Column(db.Boolean, nullable=False)
#     has_wifi = db.Column(db.Boolean, nullable=False)
#     has_sockets = db.Column(db.Boolean, nullable=False)
#     can_take_calls = db.Column(db.Boolean, nullable=False)
#     coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


    

## HTTP GET - Read Record

@app.route("/random", methods=["GET"])
def random():
    conn = sqlite3.connect('cafes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cafe ORDER BY RANDOM()')
    random_coffee = cursor.fetchone()
    print(f"Random coffee: {random_coffee}")

    return jsonify({
        "id": random_coffee[0],
        "name": random_coffee[1],
        "gmaps": random_coffee[2],
        "img_url": random_coffee[3],
        "location": random_coffee[4],
        "has_socket": random_coffee[5],
        "has_toilet": random_coffee[6],
        "wifi":random_coffee[7],
        "can_take_calls": random_coffee[8],
        "seats_available":random_coffee[9],
        "coffee_price": random_coffee[10]
        })


## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
