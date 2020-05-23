import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from sql_connection import SQLConnection

app = Flask(__name__)
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

    loginSuccessful = True

    query = ("SELECT * FROM User "
             "WHERE email=(%(email)s)")
    query_data = {'email': data["email"], }

    results = connection.query(query, query_data)
    print(results)
    if any(data["password"] not in result for result in results):
        loginSuccessful = False
    # we can add code here to query the database

    if loginSuccessful:
        return jsonify({"successfulLogin": True}), 200
    else:
        return jsonify({"error": "Invalid login credentials"}), 403


@app.route("/listing", methods=['POST'])
def listing():
    data = request.get_json()
    address = ''
    email = ''
    price = 0
    num_bedrooms = 0
    num_bathrooms = 0
    home_type = ''
    image_url = ''
    if data and "address" in data:
        address = data["address"]
    if data and "email" in data:
        email = data["email"]
    if data and "price" in data:
        price = int(data["price"])
    if data and "num_bedrooms" in data:
        num_bedrooms = int(data["num_bedrooms"])
    if data and "num_bathrooms" in data:
        num_bathrooms = int(data["num_bathrooms"])
    if data and "home_type" in data:
        home_type = data["home_type"]
    if data and "image_url" in data:
        image_url = data["image_url"]

    # save listing to database logic here

    message = 'Saved Successfully'
    if message == 'Saved Successfully':
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": "Unable to save listing"}), 404


@app.route("/getListings/<email>", methods=['GET'])
def get_listings(email):
    listing1 = Listing('233 W Whitewater Dr, Vineyard, UT 84059', 'useremail@gmail.com', 319900, 3, 2, 'Townhouse',
                       'https://photos.zillowstatic.com/cc_ft_1536/ISrxq0p3l0mh1l0000000000.webp')
    listing1_json = json.dumps(listing1.__dict__)
    listing2 = Listing('671 E 330 N, Vineyard, UT 84059', 'useremail@gmail.com', 289999, 3, 3, 'Apartment',
                       'https://photos.zillowstatic.com/cc_ft_1536/ISjn1s6wgzigqu1000000000.webp')
    listing2_json = json.dumps(listing2.__dict__)
    listings = [listing1_json, listing2_json]
    # listings_json = json.dumps(listings)
    return jsonify({"listings": [listings]}), 200


@app.route("/following/<email>", methods=['GET'])
def following(email):
    list_following = ['Jessica', 'Kyle', 'Ryan', 'Tiffany']
    json.dumps(list_following)
    return jsonify({"following": list_following}), 200


@app.route("/toFollow", methods=['POST'])
def to_follow():
    data = request.get_json()
    user = ''
    person_followed = ''
    if data and "user" in data:
        user = data["user"]
    if data and "person_followed" in data:
        person_followed = data["person_followed"]

    # add database logic here

    return jsonify({"message": "You now follow " + person_followed})


def put_dummy_data():
    tables = connection.get_tables()
    print(tables)

    add_user = ("INSERT INTO User "
                "(email, password) "
                "VALUES (%(email)s, %(password)s)")
    data_user = {
        'email': 'email@g.com',
        'password': '123abc',
    }

    connection.insert(add_user, data_user)


if __name__ == '__main__':
    global connection
    connection = SQLConnection(host="localhost", user="root", passwd="password", port=3306, db='testdb')
    if not connection.start_up():
        print(f"Couldn't connect to SQL data base")
        exit(-1)
    put_dummy_data()

    app.run(debug=True)
