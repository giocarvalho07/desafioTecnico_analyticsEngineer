# config/database.py
import mysql.connector
from mysql.connector import Error

class Config:
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER = 'root'
    DB_PASSWORD = '' # Sua senha do MySQL
    DB_NAME = 'anga_db' # O nome do seu banco de dados


def create_connection():
    """Create a database connection to the MySQL database"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            passwd=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred trying to connect to MySQL: {e}")
        # Consider logging this error
    return connection

# Se você estiver usando SQLAlchemy também, você pode adicionar o engine aqui
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# engine_dw = create_engine(
#     f"mysql+mysqlconnector://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}",
#     echo=False
# )
# SessionLocal_dw = sessionmaker(autocommit=False, autoflush=False, bind=engine_dw)