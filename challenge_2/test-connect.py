
import psycopg2
 
connection = psycopg2.connect(
    host='104.211.25.177',
    port='6666',
	database='icetruck',
	user='admin_hs',
	password='Testing1234'
	)
print('test1')
print(connection)
print('2')