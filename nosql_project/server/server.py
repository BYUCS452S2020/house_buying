import mongo_connection
import json
from mongo_connection import MongoConnection
from flask import Flask, jsonify, request

app = Flask(__name__)
database = MongoConnection()

class Listing:
    def __init__(self, address, email, price, num_bedrooms, num_bathrooms, home_type, image_url):
        self.address = address
        self.email = email
        self.price = price
        self.num_bedrooms = num_bedrooms
        self.num_bathrooms = num_bathrooms
        self.home_type = home_type
        self.image_url = image_url


@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    email = ''
    password = ''
    if data and "email" in data:
        email = data["email"]
    if data and "password" in data:
        password = data["password"]

    login_successful = database.login(email, password)

    if login_successful:
        return jsonify({"successfulLogin": True}), 200
    else:
        return jsonify({"error": "Invalid login credentials"}), 403
