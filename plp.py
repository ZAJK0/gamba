import mysql.connector
# pygame setup
mydb = mysql.connector.connect(host="localhost", user="root", password="",database="gamba")
mycursor = mydb.cursor()
mycursor.execute("select *from body")
result = mycursor.fetchone()
for i in result:
    print(i)