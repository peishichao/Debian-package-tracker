import psycopg2
conn = psycopg2.connect(database="udd",user="udd-mirror",password="udd-mirror",host="udd-mirror.debian.net",port="5432")
curs = conn.cursor()
curs.execute("SELECT count(*) from vcswatch ")
item = curs.fetchall()
conn.commit()
curs.close()
conn.close()
print item[0][0]
conn = psycopg2.connect(database="PTSdb", user="peishichao", password="123456", host="127.0.0.1", port="5432")
curs = conn.cursor()
curs.execute("SELECT count(*) from Sources_stable_main ")
item = curs.fetchall()
conn.commit()
curs.close()
conn.close()
print item[0][0]
