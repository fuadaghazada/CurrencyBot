import mysql.connector
from mysql.connector import errorcode


#import pymysql

#db = pymysql.connect("localhost","root","","test" )



# Connecting to MySQL server
try:
    connection = mysql.connector.connect(
        user = "root",
        password = "",
        host = "localhost",
        database = "TestDB"
    )
    print("Connection is Successfull!")
except mysql.connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(e)
  #      print("Something is wrong with username or password!")
    elif e.errno == errorcode.ER_BAD_DB_ERROR:
        print("DB does not exist")
    else:
        print(e)

# Creating a cursor
#cursor = connection.cursor()
