from flask import Flask, jsonify, request
app = Flask(__name__)

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

    # we can add code here to query the database

    if loginSuccessful:
        return jsonify({"successfulLogin": True}), 200
    else:
        return jsonify({"error": "Invalid login credentials"}), 403

if __name__ == '__main__':
    app.run(debug=True)