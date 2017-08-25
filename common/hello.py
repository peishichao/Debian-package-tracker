import flask
import psycopg2
import psycopg2.extensions
import select
from flask_mail import Mail, Message
from flask import session
from urlparse import urlparse, urljoin
from flask import Flask,render_template,request,flash
app = flask.Flask(__name__) 
app.secret_key = '123'
app.config.update(
    MAIL_SERVER='smtp.163.com',
    MAIL_PROT=25,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = '15630965489@163.com',
    MAIL_PASSWORD = '8068236',
    MAIL_DEBUG = True,
    secret_key = '123'
)
mail = Mail(app)
def get_sourcepackage(package_name):
	miles_dict_vcswatch = analyze_Vcswatch(package_name)
	miles_dict_sources = analyze_Sources(package_name)
	flag = True

	
	if miles_dict_vcswatch and miles_dict_sources:
		if (miles_dict_vcswatch[0] == miles_dict_sources[0][0]):
			size_sources = len(miles_dict_sources )
			'''
				1source = miles_dict_vcswatch[0]
				2version = miles_dict_vcswatch[1]
				3vsc = miles_dict_vcswatch[2]
				4url = miles_dict_vcswatch[3]
			 	5branch = miles_dict_vcswatch[4]
				6browser = miles_dict_vcswatch[5]
				7last_scan = miles_dict_vcswatch[6]
				8next_scan = miles_dict_vcswatch[7]
				9status = miles_dict_vcswatch[8]
				10debian_dir = miles_dict_vcswatch[9]
				11changelog_version = miles_dict_vcswatch[10]
				12changelog_distribution = miles_dict_vcswatch[11]
				13changelog = miles_dict_vcswatch[12]
				14error = miles_dict_vcswatch[13]
			'''
			if package_name == miles_dict_vcswatch[0] : 
				if size_sources > 1:
					flash("Source package  '"+ package_name + "' has been found by more than one version") 
				else : 
					flash("Source package  '"+ package_name + "' has been found") 
			else : 
				if size_sources > 1:
					flash("you query is  '"+ package_name + "'. Are you looking for  '" + miles_dict_vcswatch[0] + "'? if not please check you query." + "the default source package has been found by more than one version") 
				else : 
					flash("you query is  '"+ package_name + "'. Are you looking for  '" + miles_dict_vcswatch[0] + "'? if not please check you query.") 

			return render_template('search.html',**locals())
			'''
				1Package_sources = miles_dict_sources[0]
				2Binary_package_sources = miles_dict_sources[1]
				3Version_sources = miles_dict_sources[2]
				4Maintainer_sources = miles_dict_sources[3]
				5Uploaders_sources = miles_dict_sources[4]
				6Build_Depends_sources = miles_dict_sources[5]
				7Architecture_sources = miles_dict_sources[6]
				8Standards_Version_sources = miles_dict_sources[7]
				9Format_sources = miles_dict_sources[8]
				10Files_sources = miles_dict_sources[9]
				11Vcs_Browser_sources = miles_dict_sources[10]
				12Vcs_Svn_sources = miles_dict_sources[11]
				13Checksums_Sha256_sources = miles_dict_sources[12]
				14Homepage_sources = miles_dict_sources[13]
				15Package_List_sources = miles_dict_sources[14]
				16Directory_sources = miles_dict_sources[15]
				17Priority_sources = miles_dict_sources[16]
				18Section_sources = miles_dict_sources[17]	
			'''
		else :
			flash("Source package  '"+ package_name + "' not found")  
			return render_template('index.html') 
	else :
		flash("Source package  '"+ package_name + "' not found") 
		return render_template('index.html')

def analyze_Vcswatch(package_name):
	conn = psycopg2.connect(database="udd",user="udd-mirror",password="udd-mirror",host="udd-mirror.debian.net",port="5432")
    	curs = conn.cursor()
	curs.execute("SELECT * from vcswatch where source = '%s' " %package_name)
	item = curs.fetchall()
	if item :
		miles_dict = (item[0][0],item[0][1], item[0][2],item[0][3],item[0][4],
				item[0][5], item[0][6], item[0][7], item[0][8], item[0][9],
				item[0][10], item[0][11], item[0][12], item[0][13])
		conn.commit()
		curs.close()
		conn.close()
		return miles_dict
	else :
	    	curs.execute("SELECT * from vcswatch where source like '%%%%%s%%%%' " %package_name)
	    	item = curs.fetchall()
		if item : 
			print len(item),"fuzzy query Vcswatch"
			if len(item) > 1 : 
				conn.commit()
				curs.close()
				conn.close()
				return  
			else :
				miles_dict = (item[0][0],item[0][1], item[0][2],item[0][3],item[0][4],
						item[0][5], item[0][6], item[0][7], item[0][8], item[0][9],
						item[0][10], item[0][11], item[0][12], item[0][13])
				conn.commit()
				curs.close()
				conn.close()
				return miles_dict	
				
	
'''
def analyze_Sources(package_name):
	conn = psycopg2.connect(database="udd",user="udd-mirror",password="udd-mirror",host="udd-mirror.debian.net",port="5432")
    	curs = conn.cursor()
    	curs.execute("SELECT * from sources where source = '%%%%%s%%%%' " %package_name)
    	item = curs.fetchall()
	if item :
		miles_dict = (item[0][0],item[0][1], item[0][2],item[0][3],item[0][4],
				item[0][5], item[0][6], item[0][7], item[0][8], item[0][9],
				item[0][10], item[0][11], item[0][12], item[0][13],item[0][14],
				item[0][15],item[0][16],item[0][17],item[0][18],item[0][19],
				item[0][20],item[0][21],item[0][22],item[0][23],item[0][24],
				item[0][25],item[0][26],item[0][27],item[0][28],item[0][29],
				item[0][30],item[0][31],item[0][32])
	    	conn.commit()
	    	curs.close()
	    	conn.close()
		return miles_dict
'''	
def analyze_Sources(package_name):
	conn = psycopg2.connect(database="PTSdb", user="peishichao", password="123456", host="127.0.0.1", port="5432")
    	curs = conn.cursor()
    	curs.execute("SELECT * from Sources_stable_main where package like '%s' " %package_name)
    	item = curs.fetchall()
	if item :
		miles_dict = []
		for i in range(len(item)):
			if item :
				miles_dict_temp = (item[i][0],item[i][1], item[i][2],item[i][3],item[i][4],
						item[i][5], item[i][6], item[i][7], item[i][8], item[i][9],
						item[i][10], item[i][11], item[i][12], item[i][13],item[i][14],
						item[i][15],item[i][16],item[i][17])
				miles_dict.append(miles_dict_temp)
		conn.commit()
		curs.close()
		conn.close()
		return miles_dict
	else :
		curs.execute("SELECT * from Sources_stable_main where package like '%%%%%s%%%%' " %package_name)
    		item = curs.fetchall()
		if item : 
			print len(item),"fuzzy query Sources"
			if len(item) > 1 : 
				return  
			else :
				miles_dict = []
				for i in range(len(item)):
					if item :
						miles_dict_temp = (item[i][0],item[i][1], item[i][2],item[i][3],item[i][4],
								item[i][5], item[i][6], item[i][7], item[i][8], item[i][9],
								item[i][10], item[i][11], item[i][12], item[i][13],item[i][14],
								item[i][15],item[i][16],item[i][17])
						miles_dict.append(miles_dict_temp)
				conn.commit()
				curs.close()
				conn.close()
				return miles_dict				
			


def insert__subscribe_source(package_name,email_address):
	conn = psycopg2.connect(database="PTSdb", user="peishichao", password="123456", host="127.0.0.1", port="5432")
	print "Opened database successfully"
	cur = conn.cursor()
	cur.execute("SELECT * from  subscribe_source where Package = '%s' and Email = '%s' " %(package_name ,email_address))
	item = cur.fetchall()
	print item
	if item :
		conn.commit()
		conn.close()  
		return "You had subscribed this package. This operation has no result. "
	else : 
		cur.execute("""INSERT INTO subscribe_source(Package,Email)
				VALUES(%s, %s);""",
				(package_name,email_address),)
		conn.commit()
		cur.close()
		conn.close()  
		return "Data added to PostgreSQL database! "

def delete__subscribe_source(package_name,email_address):
	conn = psycopg2.connect(database="PTSdb", user="peishichao", password="123456", host="127.0.0.1", port="5432")
	print "Opened database successfully"
	cur = conn.cursor()
	cur.execute("delete  from  subscribe_source where Package = '%s' and Email = '%s' " %(package_name ,email_address))
	conn.commit()
	conn.close()  
	return "You have Deleted successfully. "

def deleteall__subscribe_source(email_address):
	conn = psycopg2.connect(database="PTSdb", user="peishichao", password="123456", host="127.0.0.1", port="5432")
	print "Opened database successfully"
	cur = conn.cursor()
	cur.execute("delete  from  subscribe_source where Email = '%s' " %email_address)
	conn.commit()
	conn.close()  
	return "You have Deleted all successfully. "


def query_by_email_address(email_address):
	conn = psycopg2.connect(database="PTSdb", user="peishichao", password="123456", host="127.0.0.1", port="5432")
	print "Opened database successfully"
	cur = conn.cursor()
	cur.execute("SELECT package from subscribe_source where Email = '%s' " %email_address)
	item = cur.fetchall()
	print item
	if item :
		conn.commit()
		conn.close()  
		return item
	
	
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
	
def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/search',methods = ['GET', 'POST'])
def search():
    if request.method == "POST":
	name = request.form.get('src')
	if name :
		print name
		return get_sourcepackage(name)
	else :
		flash("The input is empty!")  
		next = get_redirect_target()
		return render_template('index.html', next=next)

@app.route('/subscribe',methods = ['GET', 'POST'])
def subscribe():
    if request.method == "POST":
	package_name = request.values.get('packagename')
	email_address = request.form.get('email')
	if analyze_Vcswatch(package_name) and analyze_Sources(package_name):
		if email_address and  package_name:
			print package_name,email_address
			session['email'] = email_address
			responds = insert__subscribe_source(package_name,email_address)
			msg = Message("PTS Subscribe Information",sender='15630965489@163.com',recipients = [email_address] )
			msg.body = "Hi! You're welcome! You have subscribed successfully!"
			mail.send(msg)
			flash(responds) 
			return subscribe_information()
		else :
			flash("The input is illegal!")  
			next = get_redirect_target()
			return render_template('index.html', next=next)	
	else :
			flash("Source package  '"+ package_name + "' has been found") 
			return subscribe_information()

@app.route('/unsubscribe',methods = ['GET', 'POST'])
def unsubscribe():
    if request.method == "POST":
	package_name = request.form.get('packagename_unsub')
	email_address = request.form.get('email')
	if email_address and  package_name:
		print package_name,email_address
		responds = delete__subscribe_source(package_name,email_address)
		msg = Message("PTS UnSubscribe Information",sender='15630965489@163.com',recipients = [email_address] )
		msg.body = "You have unsubscribed successfully!"
		mail.send(msg)
		flash(responds) 
		flag_emails = True
		source_packages = query_by_email_address(email_address)
		if source_packages :
			flag_sources = True
			source_package_size = len(source_packages)
			return render_template('Subscriptions.html',**locals())	
			
		else : 
			flag_sources = False
			return render_template('Subscriptions.html',**locals())	
	else :
		flash("The input is illegal!")  
		next = get_redirect_target()
		return render_template('index.html', next=next)	

@app.route('/unsubscribe_all',methods = ['GET', 'POST'])
def unsubscribe_all():
    if request.method == "POST":
	email_address = request.form.get('email')
	if email_address :
		print email_address
		responds = deleteall__subscribe_source(email_address)
		msg = Message("PTS UnSubscribe Information",sender='15630965489@163.com',recipients = [email_address] )
		msg.body = "You have unsubscribed all successfully!"
		mail.send(msg)
		flash(responds) 
		flag_emails = True
		source_packages = query_by_email_address(email_address)
		if source_packages :
			flag_sources = True
			source_package_size = len(source_packages)
			return render_template('Subscriptions.html',**locals())	
			
		else : 
			flag_sources = False
			return render_template('Subscriptions.html',**locals())	
	else :
		flash("The input is illegal!")  
		next = get_redirect_target()
		return render_template('index.html', next=next)	


@app.route('/subscribe_information',methods = ['GET', 'POST'])	
def   subscribe_information():
	flag_sources = False
	flag_emails = False
	email_address = session.get('email')
	if not email_address :
		email_address = request.form.get('new_email_address')
		session['email'] = email_address
	if email_address :
		flag_emails = True
		source_packages = query_by_email_address(email_address)
		if source_packages :
			flag_sources = True
			source_package_size = len(source_packages)
			print(len(source_packages))
			return render_template('Subscriptions.html',**locals())	
		else :
			return render_template('Subscriptions.html',flag_sources = flag_sources, flag_emails = flag_emails)	
	else :
		return render_template('Subscriptions.html',flag_sources = flag_sources, flag_emails = flag_emails)	
				
	

if __name__ == "__main__":
    app.run()
