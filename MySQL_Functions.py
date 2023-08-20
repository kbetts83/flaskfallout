import mysql.connector 
from ps_db import pwsin_dict
import json

import operator
import itertools

def convert_true(value):
	if value == 1:
		return True
	else:
		return False

def connect_mysql():
	mydb =mysql.connector.connect(
		host = pwsin_dict["host"],
		user = pwsin_dict["user"],
		passwd= pwsin_dict["passwd"],
		database = pwsin_dict["database"])

	return mydb

def fetch_stores(mydb, townid):
	mycursor = mydb.cursor(dictionary = True)
	sql = """ select * from falloutstore
	where placeid = %s;
	"""

	val = (townid,)

	mycursor.execute (sql, val)
	stores = mycursor.fetchall()

	return stores

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
		sql = """SELECT falloutplace.townid , falloutplace.locationname, falloutplace.address,falloutplace.lat, falloutplace.lng, falloutplace.icon, falloutplace.description, falloutplace.draggable,
				falloutpeople.townid as people_town_id, falloutpeople.name, falloutpeople.background,falloutpeople.fact1,falloutpeople.fact2, falloutpeople.fact3,falloutpeople.hidden_person,
				falloutstore.townid as store_town_id, falloutstore.storename, falloutstore.storeid, falloutstore.storeownerid, falloutstore.storedescription, falloutstore.items,

				ABS(%s - lat) + ABS(%s - lng) AS distance
				FROM falloutplace
				left JOIN falloutpeople ON falloutpeople.townid = falloutplace.townid 
				left  JOIN falloutstore ON falloutpeople.townid = falloutstore.townid			
				ORDER BY distance;"""

		val = (lat,lng)

		mycursor.execute(sql, val)
		raw_places = mycursor.fetchall()

		#if the place isn't in the list, add it to the list
		for raw_place in raw_places:
			if raw_place['townid'] not in places_added:
				places_added.append (raw_place['townid'])
				raw_place.update({'people': [] })
				raw_place.update({"stores": [] })
				places.append(raw_place)

			if raw_place['store_town_id'] != None:
				store = {'store_town_id': raw_place['store_town_id'],  'storename' : raw_place['storename'],
				'storeid' : raw_place['storeid'], 'storeownerid' : raw_place['storeownerid'], 'storedescription' : raw_place['storedescription'],
				'items' : json.loads (raw_place['items'])
				}
				
			else:
				store = None

			if raw_place['name'] != None:
				person = {'name' : raw_place['name'], 'background' : raw_place['background'],
				'fact1' : raw_place['fact1'],'fact2' : raw_place['fact2'],'fact3' : raw_place['fact3'],
				'hidden_person': raw_place['hidden_person'], 'townid' : raw_place['people_town_id']}
			else:
				person = None 

			for pl in places:
				if person :
					if person['townid'] == pl['townid']:
						pl['people'].append (person)

				if store:
					if store['store_town_id'] == pl['townid']:
						if store not in pl['stores']:
							 
							pl['stores'].append(store)

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

def fetch_items(mydb):
	mycursor = mydb.cursor(dictionary = True)
	mycursor.execute("select * from falloutItem")

	items = mycursor.fetchall()
	return items

