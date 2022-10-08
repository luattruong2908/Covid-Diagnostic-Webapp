import sqlite3
import os
conn = sqlite3.connect('data.db', check_same_thread = False)
c = conn.cursor()

# Functions

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,name TEXT,age TEXT,phone TEXT,mail TEXT,address TEXT, sex TEXT)')


def add_userdata(username,password,name,age,phone,mail,address,sex):
	c.execute('INSERT INTO userstable(username,password,name,age,phone,mail,address,sex) VALUES (?,?,?,?,?,?,?,?)',(username,password,name,age,phone,mail,address,sex))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def displayall():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def login_user_safe2(username,password):
	c.execute("SELECT * FROM userstable WHERE username= '%s' AND password = '%s'"),(username, password);
	data = c.fetchall()
	return data

# Works but not safe agains SQL injections

def login_user_unsafe(username,password):
	c.execute("SELECT * FROM userstable WHERE username='{}' AND password = '{}'".format(username,password))
	data = c.fetchall()
	return data

def login_user_unsafe2(username,password):
	c.execute(f"SELECT * FROM userstable WHERE username= '{username}' AND password= '{password}'")
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def check_username(username):
	create_usertable()
	with conn:
		c.execute('SELECT * FROM userstable WHERE username="{}"'.format(username))
		data = c.fetchone()
		return data

def select(username, number):
	with conn:
		c.execute('SELECT * FROM userstable WHERE username="{}"'.format(username))
		data = c.fetchone()[number]
		return data

def filter_username(info):
	c.execute('SELECT * FROM userstable WHERE username="{}"'.format(info))
	data = c.fetchall()
	return data
def filter_age(info):
	c.execute('SELECT * FROM userstable WHERE age="{}"'.format(info))
	data = c.fetchall()
	return data
def filter_sex(info):
	c.execute('SELECT * FROM userstable WHERE sex="{}"'.format(info))
	data = c.fetchall()
	return data
def filter_address(info):
	c.execute('SELECT * FROM userstable WHERE address="{}"'.format(info))
	data = c.fetchall()
	return data
def filter_name(info):
	c.execute('SELECT * FROM userstable WHERE name="{}"'.format(info))
	data = c.fetchall()
	return data
def filter_phone(info):
	c.execute('SELECT * FROM userstable WHERE phone="{}"'.format(info))
	data = c.fetchall()
	return data
def filter_mail(info):
	c.execute('SELECT * FROM userstable WHERE mail="{}"'.format(info))
	data = c.fetchall()
	return data

#RESULT
def create_resultstable():
	c.execute('CREATE TABLE IF NOT EXISTS resultstable(user TEXT, result INTEGER, name TEXT, age TEXT, address TEXT, sex TEXT, image TEXT, date TEXT)')

def add_results(user,result,name,age,address,sex,image,date):
	c.execute('INSERT INTO resultstable(user, result,name,age,address,sex,image, date) VALUES (?,?,?,?,?,?,?,?)',(user, result, name, age, address, sex, image, date))
	conn.commit()

def view_all_results():
	c.execute('SELECT * FROM resultstable')
	data = c.fetchall()
	return data

def count_file():
	count = 0
	dir_path = r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Image'
	for path in os.scandir(dir_path):
		if path.is_file():
			count += 1
	return(count)

def displayall_result():
	c.execute('SELECT * FROM resultstable')
	data = c.fetchall()
	return data

def count_data(result):
	c.execute('SELECT COUNT() FROM resultstable WHERE result ="{}"'.format(result))
	data = c.fetchall()[0]
	data = int(''.join(map(str, data)))
	return data

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def filter1_username(info):
	c.execute('SELECT * FROM resultstable WHERE user="{}"'.format(info))
	data = c.fetchall()
	return data
def filter1_name(info):
	c.execute('SELECT * FROM resultstable WHERE name="{}"'.format(info))
	data = c.fetchall()
	return data
def filter1_age(info):
	c.execute('SELECT * FROM resultstable WHERE age="{}"'.format(info))
	data = c.fetchall()
	return data
def filter1_date(info):
	c.execute('SELECT * FROM resultstable WHERE date="{}"'.format(info))
	data = c.fetchall()
	return data
def filter1_sex(info):
	c.execute('SELECT * FROM resultstable WHERE sex="{}"'.format(info))
	data = c.fetchall()
	return data
def filter1_result(info):
	c.execute('SELECT * FROM resultstable WHERE result="{}"'.format(info))
	data = c.fetchall()
	return data
def filter1_address(info):
	c.execute('SELECT * FROM resultstable WHERE address="{}"'.format(info))
	data = c.fetchall()
	return data
