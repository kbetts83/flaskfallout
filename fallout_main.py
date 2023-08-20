from flask import Flask, render_template, url_for, flash, redirect,request,session

import requests, json, MySQL_Functions, googlemaps
#set the app up
app = Flask(__name__)

#set route for home pages
@app.route("/", )
def login_filter():

    #connect to mysqls
    mydb = MySQL_Functions.connect_mysql()
    here = MySQL_Functions.fetch_here(mydb)
    places = MySQL_Functions.fetch_places(mydb, False)
    items = MySQL_Functions.fetch_items(mydb) 

    return render_template('map.html', places = places, here = here, rule = 'main', items = items)

#admin page
@app.route("/admin",)
def admin_page():
    mydb = MySQL_Functions.connect_mysql()
    places = MySQL_Functions.fetch_places(mydb, True)
    here = MySQL_Functions.fetch_here(mydb)

    #get the address and then get the geocoordinates
    gmaps = googlemaps.Client(key='AIzaSyBGqQuAH6MEcprMsMH5CayhlcXda1ohDHc')

    for place in places:
        coor = gmaps.geocode(place['address'])
        lat = coor[0]["geometry"]["location"]["lat"]
        lng = coor[0]["geometry"]["location"]["lng"]
        townid = place["townid"] 

        #then if they're both floats, send them to the database
        if (isinstance(lat, float)) and (isinstance(lng, float)) :
            MySQL_Functions.write_coordinates(mydb, lat,lng, townid)
        else:
            pass

    return render_template('admin.html', places = places, here = here, rule = 'admin')


#this launches the server in debug mode
if __name__ == '__main__':
	app.run(debug=False)
