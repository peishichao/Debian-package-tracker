import psycopg2
conn = psycopg2.connect(database="PTSdb", user="peishichao", password="123456", host="127.0.0.1", port="5432")
print "Opened database successfully"
cur = conn.cursor()
cur.execute('''CREATE TABLE subscribe_source
       (ID SERIAL,Package text,Email text,PRIMARY KEY (ID));''')
print "Table created successfully"

conn.commit()
conn.close()  
