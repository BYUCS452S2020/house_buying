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

    def addListing(self, email, address, price, num_bedrooms, num_bathrooms, home_type, image_url):
        listings = self.db.listings

        listing_document = {
            "email": email,
            "address": address,
            "price": price,
            "num_bedrooms": num_bedrooms,
            "num_bathrooms": num_bathrooms,
            "home_type": home_type,
            "image_url": image_url
        }
        listings.insert_one(listing_document)

        return 'Saved Successfully'
    
    def addFollower(self, email, follow_email):
        follow = self.db.follow

        follow_document = {
            "email": email,
            "follow_email": follow_email
        }
        follow.insert_one(follow_document)

        return True


    def checkFollowingEmail(self, follow_email):
        user = self.db.user
        user_document = user.find_one({"email": follow_email})
        if user_document is None:
            return False
        else:
            return True


    def getFollowers(self, email):
        follow = self.db.follow

        return follow.find({"email": email})


    def getListings(self, email):
        listings = self.db.listings

        return listings.find({"email": email})