from pymongo import MongoClient

class MongoConnection:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://jshunt:house123@housebuying-u3icw.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client.houseBuying

    def login(self, email, password):
        # See if email and password are in database
        user = self.db.user
        user_document = user.find_one({"email": email})

        # If the email is not in the database
        if user_document is None:
            user_document = {
                "email": email,
                "password": password
            }
            user.insert_one(user_document)

        # If the user's email is in the database
        else:
            print('user document is not none')
            user_document = user.find_one({"email": email, "password": password})
            if user_document is None:
                print('incorrect password')
                return False
            else:
                print('successful login')
        return True
