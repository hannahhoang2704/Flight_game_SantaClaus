import mysql.connector                                  #fetch database
import random
from flask import Flask, request, render_template
from flask_cors import CORS
from geopy import distance                              #calculate distance geopy
#from game_project import Player
import requests
import json                                             #Json structure
from count_down import statement                        #Countdown API
from questions_func import questions_answers            #quiz function
from rock_paper_scissor import rock_paper_scissors      #rock-paper-scissors function


class Player:
    def __init__(self, name, gift=100, co2_consumption=0):
        self.name = name
        self.gift = gift
        self.co2_consumption = co2_consumption

    def get_info(self):
        return print(f"Name: {self.name}\n{self.gift} gifts\nCo2_consumption: {self.co2_consumption}")

    def get_gift(self):
        nr_random = random.randint(1, 5)
        sql = "SELECT treasure_name, score from score_change"
        sql += " WHERE id=" + str(nr_random)
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if cursor.rowcount > 0:
            for row in result:
                row[0]
                giftplus = int(row[1])
                print(f"You got {row[0]}, and earn {row[1]} gifts")
        self.gift += giftplus
        return self.gift

    def deduct_gift(self):
        nr_random = random.randint(6, 8)
        sql = "SELECT treasure_name, score from score_change"
        sql += " WHERE id=" + str(nr_random)
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if cursor.rowcount > 0:
            for row in result:
                row[0]
                giftminus = int(row[1])
                print(f"You got {row[0]}, and lost {row[1]} gifts")
        self.gift += giftminus
        return self.gift

    def co2_add(self, amount):
        self.co2_consumption += amount
        return self.co2_consumption


def fly(name = None, gift =100, consumption = 0):
    player1 = Player(name, gift, consumption)
    json_data = json.dumps(player1, indent = 4)
    return json_data

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


@app.route('/gamerinfo')
def gamerinfo():
    args = request.args
    name = args.get('name')
    location = args.get('location')
    print(name, location)
    #json_data = fly(name, 100, 0)
    sql = "INSERT into game (screen_name, location) "
    sql += "VALUES ('" + name + "','" + location + "')"
    print(sql)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    sql2 = "SELECT * from game WHERE "
    sql2 += "id=" + str(cursor.lastrowid) +";"
    print(sql2)
    cursor.execute(sql2)
    result = cursor.fetchone()
    print(result)
    ap = airport(location)
    result['airport'] = ap
    return result


def municipality_search(city):
    #icao_suggested_list = []
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
            airport_info= {}
            airport_info['ICAO'] = row[0]
            airport_info['Airport name'] = row[1]
            airport_list.append(airport_info)
        return airport_list
    #print(icao_suggested_list)
    return airport_list

#Fetch all airports in chosen city
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

@app.route('/airportdistance')
def calculate_distance_between_airports():
    args = request.args
    start_airport = fetch_airport_names_by_icao_code(args.get("start"))
    end_airport = fetch_airport_names_by_icao_code(args.get("end"))

    d = distance.distance((start_airport[2], start_airport[3]), (end_airport[2], end_airport[3])).km
    return {
        "start": (start_airport[2], start_airport[3]),
        "end": (end_airport[2], end_airport[3]),
        "dist": d
    }

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5100)
