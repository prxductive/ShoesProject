import mysql.connector
from mysql.connector import Error

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
            print("Attempting to connect...")
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to database")
        except Error as err:
            print("Connection failed")
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Invalid username or password.")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist.")
            elif err.errno == mysql.connector.errorcode.CR_CONN_HOST_ERROR:
              print("Error: Could not connect to host")
            else:
                print(f"Error: {err}")
            self.connection = None
            self.cursor = None

            #raise  # Убрать, чтобы программа не крашилась

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Disconnected from database")

    def execute_query(self, query, params=None):
        if not self.connection or not self.cursor:
            print("Error: Not connected to the database.")
            return False
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as err:
            print(f"Error executing query: {err}")
            return False

    def fetch_all(self, query, params=None):
        if not self.connection or not self.cursor:
            print("Error: Not connected to the database.")
            return None
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as err:
            print(f"Error executing query: {err}")
            return None