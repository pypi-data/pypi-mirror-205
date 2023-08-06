import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="myDB"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM orders")

rows = mycursor.fetchall()

print("City\tAmount\tGST")
for row in rows:
  print(f"{row[0]}\t{row[1]}\t{row[2]}")
