import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
from pprint import pprint
import os


class DatabaseConnection:
    """Class for all database operations."""

    def __init__(self):

        if os.getenv('DB_NAME') == 'test_db':
            self.db_name = 'test_db'
        else:
            self.db_name = 'postgres'

        try:
            self.connection = psycopg2.connect(
                dbname='postgres',host='localhost',
                port=5433, password='bekeplar', user='postgres'
                 )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.dict_cursor = self.connection.cursor(
                                            cursor_factory=RealDictCursor)

            create_user_table = """CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(50) NOT NULL,
            lastname VARCHAR(50) NOT NULL,
            othernames VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL,
            phoneNumber int,
            password TEXT NOT NULL,
            registered TEXT NOT NULL,
            isAdmin BOOL NOT NULL
                );"""
            
            create_Incidents_table = """CREATE TABLE IF NOT EXISTS incidents(
            id SERIAL NOT NULL PRIMARY KEY,
            createdBy VARCHAR(50) NOT NULL,
            type VARCHAR(50) NOT NULL,
            title VARCHAR(50) NOT NULL,
            location VARCHAR(50) NOT NULL,
            comment VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL,
            createdOn TEXT NOT NULL,
            images TEXT NOT NULL,
            videos TEXT NOT NULL
                );"""
            self.cursor.execute(create_Incidents_table)
            self.cursor.execute(create_user_table)
        except (Exception, psycopg2.DatabaseError) as error:
            pprint(error)

    def insert_redflag(self, id, createdBy,
                    type, title, location, 
                    comment, status, createdOn,
                    images, videos
                    ):
        """Method for adding a new user to users"""
        insert_redflag = """INSERT INTO incidents(
           createdBy,
           type,
           title,
           location,
           comment,
           status,
           createdOn,
           images,
           videos
            ) VALUES('{}', '{}','{}', '{}', '{}', '{}','{}', '{}', '{}')""".format(
                createdBy, type,
                title, location, comment,
                status, createdOn,
                images, videos)
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
            ) VALUES('{}', '{}','{}', '{}', '{}', '{}','{}', '{}')""".format(
                firstname, lastname,
                othernames, email, password,
                username, registered, isAdmin)
        pprint(insert_user)
        self.dict_cursor.execute(insert_user)

    def check_username(self, username):
        """
        Check if a username already exists.
        """
        query = f"SELECT * FROM users WHERE username='{username}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user
   
    def check_status(self, status):
        """
        Check if a redflag status is  editable.
        """
        query = f"SELECT * FROM incidents WHERE status='{status}';"
        pprint(query)
        self.cursor.execute(query)
        redflag = self.cursor.fetchone()
        return redflag

    def check_title(self, title):
        """
        Check if a redflag title already exists.
        """
        query = f"SELECT * FROM incidents WHERE title='{title}';"
        pprint(query)
        self.cursor.execute(query)
        redflag = self.cursor.fetchone()
        return redflag

    def check_comment(self, comment):
        """
        Check if a redflag comment already exists.
        """
        query = f"SELECT * FROM incidents WHERE comment='{comment}';"
        pprint(query)
        self.cursor.execute(query)
        redflag = self.cursor.fetchone()
        return redflag

    def check_email(self, email):
        """
        Check if a email already exists. 
        """
        query = f"SELECT * FROM users WHERE email='{email}';"
        pprint(query)
        self.dict_cursor.execute(query)
        user = self.dict_cursor.fetchone()
        return user

    def login(self, username):
        """Method to login an existing user"""
        query = "SELECT * FROM users WHERE username='{}'".format(username)
        pprint(query)
        self.dict_cursor.execute(query)
        user = self.dict_cursor.fetchone()
        return user

    def user(self, username):
        """Returning a user id from database"""
        query = "SELECT * FROM users WHERE username='{}'".format(username)
        pprint(query)
        self.dict_cursor.execute(query)
        user = self.dict_cursor.fetchone()
        return user

    def fetch_all_redflags(self):
        """Method to return all existing redflags"""
        query_all = "SELECT * FROM incidents;"
        pprint(query_all)
        self.dict_cursor.execute(query_all)
        orders = self.dict_cursor.fetchall()
        return orders

    def fetch_redflag(self, id):
        """Method to return a given redflag by its id."""
        query_one = "SELECT * FROM incidents WHERE id='{}'".format(id)
        pprint(query_one)
        self.dict_cursor.execute(query_one)
        redflag = self.dict_cursor.fetchone()
        return redflag

    def delete_redflag(self, id):
        query = "DELETE FROM incidents  WHERE id='{}'".format(id)
        pprint(query)
        self.cursor.execute(query)

    def update_status(self, id, status):
        query = "UPDATE incidents SET status='{}' WHERE id='{}'".format(status, id)
        pprint(query)
        self.cursor.execute(query)

    def update_comment(self, id, comment):
        query = """UPDATE incidents SET comment='{}' WHERE id='{}'""".format(comment, id)
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