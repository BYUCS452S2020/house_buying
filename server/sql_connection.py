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
                return False
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
        cursor.execute(where, data_dict)
        cursor.close()

    def get_tables(self):
        cursor = self.get_cursor()
        cursor.execute("SHOW TABLES")
        tables = []
        for (table, ) in cursor:
            tables.append(table)
        cursor.close()
        return tables
