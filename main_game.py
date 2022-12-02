import mysql.connector                                  #fetch database
import random
from flask import Flask, request
from flask_cors import CORS
from geopy import distance                              #calculate distance geopy

import requests
import json                                             #Json structure
from count_down import statement                        #Countdown API
from questions_func import questions_answers            #quiz function
from rock_paper_scissor import rock_paper_scissors      #rock-paper-scissors function



connection = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='game_project',
    user='root',
    password='MyN3wP4ssw0rd',  # !QAZ2wsx#EDC or MyN3wP4ssw0rd ##CHECK PASSWORD TO RUN THE PROGRAM!!!
    autocommit=True
)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

icao_suggested_list = []
def municipality_search(city):
    sql = "SELECT ident, name FROM airport"
    sql += " WHERE municipality='" + city + "'"
    # icao_list = []
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    airport_list = []
    if cursor.rowcount > 0:
        for row in result:
            print(f"      {row[0]}: {row[1]}")
            icao_suggested_list.append(row[0])       #list of ICAO code
            airport_info= {}
            airport_info['ICAO'] = row[0]
            airport_info['Airport name'] = row[1]
            airport_list.append(airport_info)
        return airport_list
    print(icao_suggested_list)
    return airport_list


@app.route('/<city>')
def airport_search(city):
    response = municipality_search(city)
    return response

def fetch_airport_names_by_icao_code(icao):
    sql  = "SELECT ID, ident, name, municipality, latitude_deg, longitude_deg FROM airport"
    sql += " WHERE ident='" + icao + "'"
    db_cursor = connection.cursor()
    db_cursor.execute(sql)
    query_result = db_cursor.fetchall()
    if db_cursor.rowcount > 0:
        for row in query_result:        # get only the first match
            return row[2], row[3], row[4], row[5]

    return "", "", "", ""

@app.route('/airport/<icao>')      # decorator
def airport(icao):
    name, location, latitude, longitude = fetch_airport_names_by_icao_code(icao)
    response = {
        "ICAO": icao,
        "Name": name,
        "Location": location,
        "Lat": latitude,
        "Long": longitude
    }
    return response

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)