from mysql import connector
from sql_connection import SQLConnection


def main():
    connection = SQLConnection(host="localhost", user="root", passwd="password", port=3306, db='testdb')
    if not connection.connect():
        connection.create_database()

    connection.create_table("CREATE TABLE User (email VARCHAR(255), password VARCHAR(255))")
    tables = connection.get_tables()
    print(tables)
    

if __name__ == "__main__":
    main()