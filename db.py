import mysql.connector

class DBManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return False

    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return None