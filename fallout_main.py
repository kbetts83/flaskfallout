from flask import Flask, render_template, url_for, flash, redirect,request,session

import json

import requests, json, MySQL_Functions

#set the app up
app = Flask(__name__)


#set route for home pages
@app.route("/", )
def login_filter():

    #connect to mysql
    mydb = MySQL_Functions.connect_mysql()
    here = MySQL_Functions.fetch_here(mydb)
    places = MySQL_Functions.fetch_places(mydb)

    return render_template('main.html', places = places, here = here)

#this launches the server in debug mode
if __name__ == '__main__':
	app.run(debug=False)
