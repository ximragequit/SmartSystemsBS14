import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user='postgres', password='testing1234', host='192.168.4.181', port= '5432'
)

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Executing an MYSQL function using the execute() method
cursor.execute("select version()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Connection established to: ",data)


#Adding Data
insert_stmt = (
   "INSERT INTO table(column 1, column 2, column 3)"
   "VALUES (%s, %s, %s)"
)
data = ('value 1', 'value 2', 'value 3')

try:
   # Executing the SQL command
   cursor.execute(insert_stmt, data)
   
   # Commit your changes in the database
   conn.commit()

except:
   # Rolling back in case of error
   conn.rollback()

print("Data inserted")
print(insert_stmt, data)

#Closing the connection
conn.close()#

