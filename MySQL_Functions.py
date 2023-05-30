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

def fetch_places(mydb, empty_coor):
	mycursor = mydb.cursor(dictionary=True)
	if empty_coor == False:

		#get the latitude and longitude of here - kind of dumb but i'm getting frustrated
		mycursor.execute ("select lat from falloutplace where locationname = 'here' ")
		lat = mycursor.fetchall()[0]["lat"]
		mycursor.execute ("select lng from falloutplace where locationname = 'here' ")
		lng = mycursor.fetchall()[0]["lng"]

		mycursor = mydb.cursor(dictionary=True)
		sql = """SELECT *, ABS(%s - lat) + ABS(%s - lng) AS distance
				FROM falloutplace
				WHERE hidden = 0
				ORDER BY distance;"""

		val = (lat,lng)

		mycursor.execute(sql, val)
		places = mycursor.fetchall()

	if empty_coor == True:
		mycursor.execute ("select * from falloutplace where lat is null or lng is null")	
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

def write_coordinates(mydb, lat,lng, townid):
	mycursor = mydb.cursor()
	sql = "UPDATE falloutplace SET lat = (%s),lng =  (%s) WHERE townid = (%s);"
	val = (lat,lng,townid)

	mycursor.execute(sql, val)

	mydb.commit()

mydb = connect_mysql()
butt = fetch_places(mydb, 0)
for b in butt:
	print (b)
	print ("")