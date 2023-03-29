import mysql.connector


class Database:
    
    def __init__(self, host, user, passwd):
        self.con = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database="kannagi"
        )

    def execute(self, query, *parameters, commit = False):
        cursor = self.con.cursor()
        cursor.execute(query, parameters)
        if commit:
            self.con.commit()
        return cursor.fetchall()