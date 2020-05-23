from mysql import connector
from mysql.connector import errorcode


class SQLConnection:
    def __init__(self, host="localhost", user="root", passwd="password", port=3306, db='testdb'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db = db
        self.connection = None

    def start_up(self):
        if not self.connect():
            if not self.create_database():
                return False
        # self.get_cursor().execute("DROP TABLE Following")
        self.create_table("CREATE TABLE User "
                          "(email VARCHAR(255) NOT NULL,"
                          " password VARCHAR(255) NOT NULL,"
                          " PRIMARY KEY (email))")
        if not self.create_table("CREATE TABLE Listing"
                                 "(email VARCHAR(255) NOT NULL,"
                                 " address VARCHAR(255),"
                                 " price INT,"
                                 " num_bedrooms INT,"
                                 " num_bathrooms INT,"
                                 " home_type VARCHAR(255),"
                                 " image_url VARCHAR(255),"
                                 " FOREIGN KEY (email)"
                                 " REFERENCES User (email))"):
            return False
        if not self.create_table("CREATE TABLE Following "
                                 "(email VARCHAR(255) NOT NULL,"
                                 " follow_email VARCHAR(255) NOT NULL,"
                                 " FOREIGN KEY (email)"
                                 " References User (email),"
                                 " FOREIGN KEY (follow_email)"
                                 " REFERENCES User (email),"
                                 " PRIMARY KEY (email, follow_email))"):
            return False
        return True

    def connect(self):
        try:
            self.connection = connector.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port,
                                                db=self.db)
        except connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                return False
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist, try func create_database")
                return False
            else:
                print(err)
                return False
        return True

    def create_database(self):
        try:
            self.connection = connector.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
        except connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                return False
            else:
                print(err)
                return False
        cursor = self.connection.cursor()
        cursor.execute(f"CREATE DATABASE {self.db}")
        cursor.close()
        return self.connect()

    def create_table(self, table_str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(table_str)
            cursor.close()
        except connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
                return True
            else:
                print(err.msg)
                return False
        else:
            print("Table made")
            return True

    def get_cursor(self):
        return self.connection.cursor()

    def insert(self, where, data_dict):
        cursor = self.connection.cursor()
        try:
            cursor.execute(where, data_dict)
        except connector.Error as err:
            if err.errno == 1062:  # dubplicate entry
                print('data not inserted, already in table.')
                return False
            else:
                raise err

        self.connection.commit()
        cursor.close()
        return True

    def get_tables(self):
        cursor = self.get_cursor()
        cursor.execute("SHOW TABLES")
        tables = []
        for (table, ) in cursor:
            tables.append(table)
        cursor.close()
        return tables
    
    def query(self, query, query_data):
        cursor = self.connection.cursor()
        cursor.execute(query, query_data)
        query_results = []
        for result in cursor:
            query_results.append(result)
        cursor.close()
        return query_results
