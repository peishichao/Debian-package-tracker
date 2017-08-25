import psycopg2
conn = psycopg2.connect(database="PTSdb", user="peishichao", password="123456", host="127.0.0.1", port="5432")
print "Opened database successfully"
cur = conn.cursor()
cur.execute('''CREATE TABLE Sources_stable_main
       (Package	text,Binary_package text,Version text,Maintainer text,Uploaders text,Build_Depends text,Architecture text,Standards_Version text,Format text,Files text,Vcs_Browser text,Vcs_Svn text,Checksums_Sha256 text,Homepage text,Package_List text,Directory text,Priority text,Section text,PRIMARY KEY (Package,Binary_package,Version));''')
print "Table created successfully"

conn.commit()
conn.close()  
