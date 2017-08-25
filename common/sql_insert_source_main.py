import psycopg2
conn = psycopg2.connect(database="PTSdb", user="peishichao", password="123456", host="127.0.0.1", port="5432")
print "Opened database successfully"
cur = conn.cursor()
file = open("/home/steven/Desktop/common/data/Sources-stable_main")

flag = False
Package_list = []
Binary_package_list = []
Version_list = []
Maintainer_list = []
Uploaders_list = []
Build_Depends_list = []
Architecture_list = []
Standards_Version_list = []
Format_list = []
Files_list = []
Vcs_Browser_list = []
Vcs_Svn_list = []
Checksums_Sha256_list = []
Homepage_list = []
Package_List_list = []
Directory_list = []
Priority_list = []
Section_list = []
flag = False
while 1:
	line = file.readline()
	if not line:
		break
	line=line.strip('\n')
	information_data_title = line.split(':',1)[0]
	information_data = line.split(':',1)[-1].strip(' ')
	if (information_data_title == "Package"):
		Package_list.append(information_data)
		Vcs_Svn_list.append("null")
		flag = True
	while flag and (information_data_title == "Binary") and (len(Binary_package_list) < len(Package_list)-1):
		Binary_package_list.append("null") 
	if flag and (information_data_title == "Binary") and (len(Binary_package_list) == len(Package_list)-1):
		Binary_package_list.append(information_data) 
	while flag and (information_data_title == "Version") and (len(Version_list) < len(Package_list)-1):
		Version_list.append("null")
	if flag and (information_data_title == "Version") and (len(Version_list) == len(Package_list)-1):
		Version_list.append(information_data)
	while flag and (information_data_title == "Maintainer") and (len(Maintainer_list) < len(Package_list)-1):
		Maintainer_list.append("null")
	if flag and (information_data_title == "Maintainer") and (len(Maintainer_list) == len(Package_list)-1):
		Maintainer_list.append(information_data)
	while flag and (information_data_title == "Uploaders") and (len(Uploaders_list) < len(Package_list)-1):
		Uploaders_list.append("null")
	if flag and (information_data_title == "Uploaders") and (len(Uploaders_list) == len(Package_list)-1):
		Uploaders_list.append(information_data)
	while flag and (information_data_title == "Build-Depends") and (len(Build_Depends_list) < len(Package_list)-1):
		Build_Depends_list.append("null")
	if flag and (information_data_title == "Build-Depends") and (len(Build_Depends_list) == len(Package_list)-1):
		Build_Depends_list.append(information_data)

	while flag and (information_data_title == "Architecture") and (len(Architecture_list) < len(Package_list)-1):
		Architecture_list.append("null")
	if flag and (information_data_title == "Architecture") and (len(Architecture_list) == len(Package_list)-1):
		Architecture_list.append(information_data)

	while flag and (information_data_title == "Standards-Version") and (len(Standards_Version_list) < len(Package_list)-1):
		Standards_Version_list.append("null")
	if flag and (information_data_title == "Standards-Version") and (len(Standards_Version_list) == len(Package_list)-1):
		Standards_Version_list.append(information_data)

	while flag and (information_data_title == "Format") and (len(Format_list) < len(Package_list)-1):
		Format_list.append("null")
	if flag and (information_data_title == "Format") and (len(Format_list) == len(Package_list)-1):
		Format_list.append(information_data)

	while flag and (information_data_title == "Files") and (len(Files_list) < len(Package_list)-1):
		Files_list.append("null")
	if flag and (information_data_title == "Files") and (len(Files_list) == len(Package_list)-1):
		Files_list.append(information_data)

	while flag and (information_data_title == "Vcs-Browser") and (len(Vcs_Browser_list) < len(Package_list)-1):
		Vcs_Browser_list.append("null")
	if flag and (information_data_title == "Vcs-Browser") and (len(Vcs_Browser_list) == len(Package_list)-1):
		Vcs_Browser_list.append(information_data)
	'''
	while flag and (information_data_title == "Vcs-Svn") and (len(Vcs_Svn_list) < len(Package_list)-1):
		Vcs_Svn_list.append("null")
	if flag and (information_data_title == "Vcs-Svn") and (len(Vcs_Svn_list) == len(Package_list)-1):
		Vcs_Svn_list.append(information_data)
	'''
	while flag and (information_data_title == "Checksums-Sha256") and (len(Checksums_Sha256_list) < len(Package_list)-1):
		Checksums_Sha256_list.append("null")
	if flag and (information_data_title == "Checksums-Sha256") and (len(Checksums_Sha256_list) == len(Package_list)-1):
		Checksums_Sha256_list.append(information_data)

	while flag and (information_data_title == "Homepage") and (len(Homepage_list) < len(Package_list)-1):
		Homepage_list.append("null")
	if flag and (information_data_title == "Homepage") and (len(Homepage_list) == len(Package_list)-1):
		Homepage_list.append(information_data)

	while flag and (information_data_title == "Package-List") and (len(Package_List_list) < len(Package_list)-1):
		Package_List_list.append("null")
	if flag and (information_data_title == "Package-List") and (len(Package_List_list) == len(Package_list)-1):
		Package_List_list.append(information_data)

	while flag and (information_data_title == "Directory") and (len(Directory_list) < len(Package_list)-1):
		Directory_list.append("null")
	if flag and (information_data_title == "Directory") and (len(Directory_list) == len(Package_list)-1):
		Directory_list.append(information_data)

	while flag and (information_data_title == "Priority") and (len(Priority_list) < len(Package_list)-1):
		Priority_list.append("null")
	if flag and (information_data_title == "Priority") and (len(Priority_list) == len(Package_list)-1):
		Priority_list.append(information_data)

	while flag and (information_data_title == "Section") and (len(Section_list) < len(Package_list)-1):
		Section_list.append("null")
	if flag and (information_data_title == "Section") and (len(Section_list) == len(Package_list)-1):
		Section_list.append(information_data)

print len(Section_list),len(Package_list),len(Priority_list),len(Directory_list) ,len(Package_List_list),len(Homepage_list),len(Checksums_Sha256_list),len(Vcs_Svn_list),len(Vcs_Browser_list),len(Files_list),len(Format_list),len(Standards_Version_list),len(Architecture_list),len(Build_Depends_list),len(Uploaders_list),len(Maintainer_list),len(Version_list),len(Version_list)

for i in range(len(Package_list)):
	cur.execute("""INSERT INTO Sources_stable_main          	(Package,Binary_package,Version,Maintainer,Uploaders,Build_Depends,Architecture,Standards_Version,Format,Files,Vcs_Browser,Vcs_Svn,Checksums_Sha256,Homepage,Package_List,Directory,Priority,Section)
		        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
		        (Package_list[i],
		        Binary_package_list[i],
		        Version_list[i],
		        Maintainer_list[i],
		        Uploaders_list[i],
		        Build_Depends_list[i],
		        Architecture_list[i],
		        Standards_Version_list[i],
		        Format_list[i],
		        Files_list[i],
		        Vcs_Browser_list[i],
		        Vcs_Svn_list[i],
		        Checksums_Sha256_list[i],
			Homepage_list[i],
			Package_List_list[i],
			Directory_list[i],
			Priority_list[i],
			Section_list[i]),)
conn.commit()
print "Data added to PostgreSQL database!"

conn.close()  
