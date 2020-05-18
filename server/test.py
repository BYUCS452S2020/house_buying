from mysql import connector
from sql_connection import SQLConnection


def main():
    connection = SQLConnection(host="localhost", user="root", passwd="password", port=3306, db='testdb')
    if not connection.connect():
        connection.create_database()

    connection.create_table("CREATE TABLE User (email VARCHAR(255) NOT NULL,"
                            " password VARCHAR(255) NOT NULL,"
                            " PRIMARY KEY (email))")
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

    query = ("SELECT * FROM User "
             "WHERE email=(%(email)s)")
    query_data = {'email': 'email@g.com', }

    results = connection.query(query, query_data)
    print(results)


if __name__ == "__main__":
    main()
