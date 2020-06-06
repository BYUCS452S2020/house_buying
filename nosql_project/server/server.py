import mongo_connection
import json
from mongo_connection import MongoConnection
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
database = MongoConnection()
CORS(app)

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


@app.route("/listing", methods=['POST'])
def listing():
    data = request.get_json()
    if data and "email" in data:
        email = data["email"]
    if data and "address" in data:
        address = data["address"]
    if data and "price" in data:
        price = data["price"]
    if data and "num_bedrooms" in data:
        num_bedrooms = data["num_bedrooms"]
    if data and "num_bathrooms" in data:
        num_bathrooms = data["num_bathrooms"]
    if data and "home_type" in data:
        home_type = data["home_type"]
    if data and "image_url" in data:
        image_url = data["image_url"]

    message = database.addListing(email, address, price, num_bedrooms, num_bathrooms, home_type, image_url)

    if message == 'Saved Successfully':
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": "Unable to save listing"}), 404


@app.route("/toFollow", methods=['POST'])
def to_follow():
    data = request.get_json()
    user = ''
    person_followed = ''
    if data and "user" in data:
        user = data["user"]
    if data and "person_followed" in data:
        person_followed = data["person_followed"]
    if user == person_followed:
        return jsonify({"message": f"You can't follow yourself."})

    results = database.checkFollowingEmail(person_followed)
    if results == False:
        return jsonify({"message": f"{person_followed} is not an email in the database."})

    if not database.addFollower(user, person_followed):
        return jsonify({"message": "Unable to complete request"})

    return jsonify({"message": "You now follow " + person_followed})


@app.route("/following/<email>", methods=['GET'])
def following(email):
    results = database.getFollowers(email)
    list_following = []

    for obj in results:
        list_following.append(obj['follow_email'])
        
    return jsonify({"following": list_following}), 200


@app.route("/getListings/<email>", methods=['GET'])
def get_listings(email):
    results = database.getListings(email)
    result_json = []
    for obj in results:
        temp_listing = Listing(obj['address'],obj['email'], obj['price'],obj['num_bedrooms'],obj['num_bathrooms'],obj['home_type'],obj['image_url'])
        result_json.append(json.dumps(temp_listing.__dict__))

    listings = result_json
    # listings_json = json.dumps(listings)
    return jsonify({"listings": [listings]}), 200

if __name__ == '__main__':

    app.run(debug=True)
