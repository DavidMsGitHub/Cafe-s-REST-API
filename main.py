from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

# CONNECITON TO DATABASE FUNCTION

def connect_db():
    return sqlite3.connect("cafes.db")

#--------#_------------#_---------------


# -----_-__-WAS SQLALCHEMY IN ORIGINAL PROJECT START-----_-__-
#
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
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cafe ORDER BY RANDOM()')
    random_coffee = cursor.fetchone()
    columns = [description[0] for description in cursor.description]
    coffee_data = dict(zip(columns, random_coffee))

    return jsonify(cafe=coffee_data)


@app.route("/all", methods=["GET"])
def all():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cafe')
    coffee_data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    all_coffees = [dict(zip(columns, i)) for i in coffee_data]
    return jsonify(all_coffees)

@app.route("/search", methods=["GET"])
def search():
    location = request.args.get("loc")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cafe WHERE location = ?", (location,))
    coffee_data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    all_c = [dict(zip(columns, i)) for i in coffee_data]
    if all_c:
        return jsonify({f"Cafes in {location}": all_c})
    else:

        return jsonify(error={"No cafe found": "Sorry, no cafe found on this location."})

## HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def add_cafe():
    r = request.form
    print(r["name"])
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO cafe (name, location, map_url, img_url, has_sockets, has_wifi, has_toilet, can_take_calls, seats, coffee_price) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
        ''', (r["name"], r["location"], r["map_url"], r["img_url"], r["has_sockets"], r["has_wifi"], r["has_toilet"], r["can_take_calls"], r["seats"], r["coffee_price"]) )
    conn.commit()
    return jsonify(success={
        "Successful": "added cafe to the database"
    })



## HTTP PUT/PATCH - Update Record

@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cafe SET coffee_price = ? WHERE id = ?", (new_price, cafe_id))
    cursor.execute("SELECT * FROM cafe WHERE id = ?", (cafe_id,))
    conn.commit()
    cafe = cursor.fetchone()
    if cafe:
        return jsonify(success=f"Successfully updated price for cafe {cafe[1]}")
    else:
        return jsonify(error={"No cafe found": "Sorry, no cafe found"})


## HTTP DELETE - Delete Record

@app.route("/delete-cafe/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    conn = connect_db()
    cursor = conn.cursor()
    if request.args.get("api_key") == "topsecret":
        cursor.execute("SELECT * FROM cafe WHERE id = ?", (cafe_id,))
        gela = cursor.fetchone()
        if gela:
            cursor.execute("DELETE FROM cafe WHERE id = ?", (cafe_id,))
            conn.commit()
            return jsonify(success=f"Successfully deleted cafe {gela[1]}")
        else:
            return jsonify(error={"No cafe found": "Sorry, no cafe with this id found"})
    else:
        return jsonify(error="You got an Invalid API Key")


if __name__ == '__main__':
    app.run(debug=True)
