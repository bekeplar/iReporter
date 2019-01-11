import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
from pprint import pprint
import os


class DatabaseConnection:
    """Class for all database operations."""

    def __init__(self):

        try:
            self.connection = psycopg2.connect(
                dbname='travis_ci_test'
                 )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.dict_cursor = self.connection.cursor(
                                            cursor_factory=RealDictCursor)

            create_Incidents_table = """CREATE TABLE IF NOT EXISTS Incidents(
            id SERIAL NOT NULL PRIMARY KEY,
            createdBy TEXT NOT NULL,
            type FLOAT NOT NULL,
            title TEXT NOT NULL, 
            location TEXT NOT NULL, 
            comment TEXT NOT NULL,
            createdOn TIMESTAMP
            images VARCHAR(50) NOT NULL,
            videos TEXT NOT NULL,
                );"""
            create_user_table = """CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(50) NOT NULL,
            lastname VARCHAR(50) NOT NULL,
            othernames VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL,
            useremail VARCHAR(50) NOT NULL,
            phoneNumber bigint NOT NULL,
            password TEXT NOT NULL,
            registered TEXT NOT NULL,
            isAdmin BOOL NOT NULL
                );"""
            self.cursor.execute(create_Incidents_table)
            self.cursor.execute(create_user_table)
        except (Exception, psycopg2.DatabaseError) as error:
            pprint(error)

    def insert_redflag(self, *args):
        createdBy = args[0]
        type = args[1]
        title = args[2]
        location = args[3]
        comment = args[4]
        status = args[5]
        createdOn = args[6]
        images = args[7]
        videos = args[8]

        """Method for adding a new redflag to incidents"""
        insert_redflag = """INSERT INTO Incidents(
            createdBy,
            type,
            title,
            location,
            comment,
            status,
            createdOn,
            images,
            videos
            ) VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}''{}', '{}')""".format(
            createdBy,
            type,
            title,
            location,
            comment,
            status,
            createdOn,
            images,
            videos
        )
        pprint(insert_redflag)
        self.dict_cursor.execute(insert_redflag)

    def insert_user(self, id, firstname, lastname,
                    othernames, email, password,
                    username, registered, isAdmin
                    ):
        """Method for adding a new user to users"""
        insert_user = """INSERT INTO users(
           firstname,
           lastname,
           othernames,
           email,
           password,
           username,
           registered,
           isAdmin
            ) VALUES('{}', '{}','{}', '{}', '{}', '{}','{}', '{}')""".format(firstname, lastname,
                                                                             othernames, email, password,
                                                                             username, registered, isAdmin)
        pprint(insert_user)
        self.dict_cursor.execute(insert_user)

    def login(self, username):
        """Method to login an existing user"""
        query = "SELECT * FROM users WHERE name='{}'".format(username)
        pprint(query)
        self.dict_cursor.execute(query)
        user = self.dict_cursor.fetchone()
        return user

    def check_email(self, email):
        query = "SELECT * FROM users WHERE email='{}'".format(email)
        pprint(query)
        self.dict_cursor.execute(query)
        user = self.dict_cursor.fetchone()
        return user

    def user(self, name):
        """Returning a user id from database"""
        query = "SELECT * FROM users WHERE name='{}'".format(name)
        pprint(query)
        self.dict_cursor.execute(query)
        user = self.dict_cursor.fetchone()
        return user

    def fetch_all_redflags(self):
        """Method to return all existing redflags"""
        query_all = "SELECT * FROM incidents WHERE type='redflag'"
        pprint(query_all)
        self.dict_cursor.execute(query_all)
        orders = self.dict_cursor.fetchall()
        return orders

    def fetch_redflag(self, id):
        """Method to return a given redflag by its id."""
        query_one = "SELECT * FROM Incidents WHERE id='{}'".format(id)
        pprint(query_one)
        self.dict_cursor.execute(query_one)
        redflag = self.dict_cursor.fetchone()
        return redflag

    def delete_redflag(self, id):
        query = "DELETE* FROM Incidents  WHERE id='{}'".format(id)
        pprint(query)
        self.cursor.execute(query)

    def update_status(self, id, status):
        query = "UPDATE Incidents SET status='{}' WHERE id='{}'".format(status, id)
        pprint(query)
        self.cursor.execute(query)

    def update_comment(self, id, comment):
        query = """UPDATE Incidents SET comment='{}' WHERE id='{}'""".format(comment, id)
        pprint(query)
        self.dict_cursor.execute(query)

    def update_location(self, id, location):
        """Method to edit  redflag location."""
        query = """UPDATE incidents SET location='{}' WHERE id='{}'""".format(location, id)
        pprint(query)
        self.dict_cursor.execute(query)

    def create_admin(self, userId, admin):
        "Method to create an admin"
        query = """UPDATE  users SET admin='{}' WHERE userId='{}'""".format(True, userId)
        pprint(query)
        self.dict_cursor.execute(query)

    def drop_tables(self):
        drop = "DROP TABLE Incidents, users"
        pprint(drop)
        self.cursor.execute(drop)


if __name__ == '__main__':
    database_connection = DatabaseConnection()
# self.connection = psycopg2.connect(
# dbname = os.environ["DATABASE_URL"]
# dbname='travis_ci_test'                       