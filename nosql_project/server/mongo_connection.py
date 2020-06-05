from pymongo import MongoClient

class MongoConnection:
    client = MongoClient("mongodb+srv://jshunt:house123@housebuying-u3icw.mongodb.net/test?retryWrites=true&w=majority")
    db = client.houseBuying

    def login(self, email, password):
        # See if email and password are in database
        user = db.user
        user_document = user.find_one({"email": email})

        if userRecord is None:
            user_document = {
                "email": email,
                "password": password
            }
            user.insert_one(user_document)
        return true
