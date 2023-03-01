import mysql.connector 
from ps_db import pwsin_dict
import json

def connect_mysql():
	mydb =mysql.connector.connect(
		host = pwsin_dict["host"],
		user = pwsin_dict["user"],
		passwd= pwsin_dict["passwd"],
		database = pwsin_dict["database"])

	return mydb

def fetch_places(mydb):
	mycursor = mydb.cursor(dictionary=True)
	mycursor.execute ("select * from falloutplace where hidden = 0")	
	places = mycursor.fetchall()
	return places

def fetch_people(mydb, place):
	mycursor = mydb.cursor(dictionary=True)
	place = place
	sql = "select * from falloutpeople where townID = %s"
	var = (1, )
	mycursor.execute (sql, var)
	people = mycursor.fetchall()
	return people

def fetch_here(mydb):
	mycursor = mydb.cursor(dictionary=True)
	mycursor.execute ("select lng, lat from falloutplace where locationname = 'here'")	
	here = mycursor.fetchall()
	return here[0]
