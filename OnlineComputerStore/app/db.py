import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='newarkit_dev_user',
        password='newarkitdev',
        database='newarkit_dev'
    )
