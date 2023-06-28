import mysql.connector 
from ps_db import pwsin_dict
import json

import operator
import itertools

def add_people(place):

		return place

def connect_mysql():
	mydb =mysql.connector.connect(
		host = pwsin_dict["host"],
		user = pwsin_dict["user"],
		passwd= pwsin_dict["passwd"],
		database = pwsin_dict["database"])

	return mydb

def fetch_places(mydb, empty_coor):

	places = []
	places_added = []

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
				left join falloutpeople on falloutplace.townid = falloutpeople.townid
				WHERE hidden = 0
				ORDER BY distance;"""

		val = (lat,lng)

		mycursor.execute(sql, val)
		raw_places = mycursor.fetchall()
		for p in range(len(raw_places)):
			place = {"townid" : raw_places[p]['townid'], 'locationName' : raw_places[p]['locationName'],
					"address" : raw_places[p]['address'], 'lat' : raw_places[p]['lat'], "lng" : raw_places[p]['lng'],
					"icon" : raw_places[p]['icon'], 'description' : raw_places[p]['description'],'distance' : raw_places[p]['distance'], 'people' : []
			  }
			people = {'townID': raw_places[p]['townid'], 'name': raw_places[p]['name'], 'background': raw_places[p]['background'], 
			'fact1': raw_places[p]['fact1'], 'fact2': raw_places[p]['fact2'], 'fact3': raw_places[p]['fact3']}

			#check if that place exists, if it doesn't add it to the list
			if place['townid'] not in places_added:
				places_added.append(place['townid'])
				places.append(place)

			#and then add that person to the place if there's a person
			if people['name']:
				for pl in places:
					if pl['townid'] == people['townID']:
						pl['people'].append(people)

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

db = connect_mysql()
butt= fetch_places(db, 0)


