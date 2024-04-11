import pymysql



class DbHandler:
    def __init__(self):
        # Replace these with your actual database credentials
        self.host = '127.0.0.1'
        self.user = 'usersomething'
        self.password = 'passwordwhoseawhatsit'
        self.database = 'acore_world'

        # Establish connection
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def insert_rows(self):
        # Example INSERT statement
        insert_query = "INSERT INTO your_table_name (column1, column2, column3) VALUES (%s, %s, %s)"

        # Example data values
        data_values = ('value1', 'value2', 'value3')

        # Execute the INSERT query with data values
        self.cursor.execute(insert_query, data_values)

        # Commit changes to the database
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()



