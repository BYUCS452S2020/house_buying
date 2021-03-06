import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from sql_connection import SQLConnection

app = Flask(__name__)
CORS(app)
PERFECT_HOUSE_URL = "http://d21c.com/DragonsDreams/unicorns/Rainbow_World.jpg"
PERFECT_HOUSE_ADDRESS = "Ideal House"


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

    login_successful = True

    query = ("SELECT * FROM User "
             "WHERE email=(%(email)s)")
    query_data = {'email': email, }

    results = connection.query(query, query_data)
    print(len(results))
    if any(password not in result for result in results) or len(results) == 0:
        login_successful = False
        add_user = ("INSERT INTO User "
                    "(email, password) "
                    "VALUES (%(email)s, %(password)s)")

        if connection.insert(add_user, data):
            login_successful = True

    if login_successful:
        return jsonify({"successfulLogin": True}), 200
    else:
        return jsonify({"error": "Invalid login credentials"}), 403


@app.route("/listing", methods=['POST'])
def listing():
    data = request.get_json()

    format_str = ("INSERT INTO Listing "
                  "(email, address, price, num_bedrooms, num_bathrooms, home_type, image_url) "
                  "VALUES (%(email)s, %(address)s, %(price)s, %(num_bedrooms)s, %(num_bathrooms)s, %(home_type)s, "
                  "%(image_url)s)")

    message = 'Saved Successfully'

    if not connection.insert(format_str, data):
        message = ' '

    if message == 'Saved Successfully':
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": "Unable to save listing"}), 404


@app.route("/perfect", methods=['POST'])
def perfect():
    data = request.get_json()

    format_str = ("INSERT INTO Listing "
                  "(email, address, price, num_bedrooms, num_bathrooms, home_type, image_url) "
                  "VALUES (%(email)s, %(address)s, %(price)s, %(num_bedrooms)s, %(num_bathrooms)s, %(home_type)s, "
                  "%(image_url)s)")

    data['address'] = PERFECT_HOUSE_ADDRESS
    data['image_url'] = PERFECT_HOUSE_URL
    message = 'Saved Successfully'

    if not connection.insert(format_str, data):
        message = ' '

    if message == 'Saved Successfully':
        print(message)
        return jsonify({"message": message}), 200
    else:
        print(message)
        return jsonify({"message": "Unable to save listing"}), 404


@app.route("/getListings/<email>", methods=['GET'])
def get_listings(email):
    query = ("SELECT address, email, price, num_bedrooms, num_bathrooms, home_type, image_url FROM Listing "
             "WHERE email=(%(email)s)")
    query_data = {'email': email, }

    results = connection.query(query, query_data)
    result_json = []
    for result in results:
        print(result)
        temp_listing = Listing(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        result_json.append(json.dumps(temp_listing.__dict__))
    listing1 = Listing('233 W Whitewater Dr, Vineyard, UT 84059', 'useremail@gmail.com', 319900, 3, 2, 'Townhouse',
                       'https://photos.zillowstatic.com/cc_ft_1536/ISrxq0p3l0mh1l0000000000.webp')
    listing1_json = json.dumps(listing1.__dict__)
    listing2 = Listing('671 E 330 N, Vineyard, UT 84059', 'useremail@gmail.com', 289999, 3, 3, 'Apartment',
                       'https://photos.zillowstatic.com/cc_ft_1536/ISjn1s6wgzigqu1000000000.webp')

    listing2_json = json.dumps(listing2.__dict__)
    # listings = [listing1_json, listing2_json] + result_json
    listings = result_json
    # listings_json = json.dumps(listings)
    return jsonify({"listings": [listings]}), 200


@app.route("/following/<email>", methods=['GET'])
def following(email):
    query = ("SELECT follow_email FROM Following "
             "WHERE email=(%(email)s)")
    query_data = {'email': email, }

    results = connection.query(query, query_data)
    print(results)
    # list_following = ['Jessica', 'Kyle', 'Ryan', 'Tiffany']
    list_following = []

    for result in results:
        list_following.append(result)
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
    if user == person_followed:
        return jsonify({"message": f"You can't follow yourself."})

    query = ("SELECT * FROM User "
             "WHERE email=(%(email)s)")
    query_data = {'email': person_followed, }

    results = connection.query(query, query_data)
    if len(results) == 0:
        return jsonify({"message": f"{person_followed} is not an email in the database."})

    query = ("SELECT follow_email FROM Following "
             "WHERE email=(%(email)s)")
    query_data = {'email': user, }

    results = connection.query(query, query_data)
    if any(person_followed in result for result in results):
        return jsonify({"message": f"{user} already follows{person_followed}."})

    add_follow = ("INSERT INTO Following "
                  "(email, follow_email) "
                  "VALUES (%(email)s, %(follow_email)s)")
    data_user = {
        'email': user,
        'follow_email': person_followed,
    }
    if not connection.insert(add_follow, data_user):
        return jsonify({"message": "Unable to complete request"})

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

    data_user = {
        'email': 'g@g.com',
        'password': 'password',
    }
    connection.insert(add_user, data_user)

    data_user = {
        'email': 'q@g.com',
        'password': 'password',
    }
    connection.insert(add_user, data_user)

    data_user = {
        'email': 'test@g.com',
        'password': 'password',
    }
    connection.insert(add_user, data_user)

    add_follow = ("INSERT INTO Following "
                  "(email, follow_email) "
                  "VALUES (%(email)s, %(follow_email)s)")
    data_user = {
        'email': 'email@g.com',
        'follow_email': 'g@g.com',
    }
    connection.insert(add_follow, data_user)

    data_user = {
        'email': 'email@g.com',
        'follow_email': 'q@g.com',
    }
    connection.insert(add_follow, data_user)


if __name__ == '__main__':
    global connection
    connection = SQLConnection(host="localhost", user="root", passwd="password", port=3306, db='testdb')
    if not connection.start_up():
        print(f"Couldn't connect to SQL data base")
        exit(-1)
    put_dummy_data()

    app.run(debug=True)
