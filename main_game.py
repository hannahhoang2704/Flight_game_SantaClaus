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


def questions_answers():

    # Questionaires and answers
    questions = (
        "Wasting less food is a way to reduce greenhouse gas emissions.",  # 0
        "The overwhelming majority of scientists agree that climate change is real and caused by humans.",
        # 1
        "Combustion removes carbon from the atmosphere",  # 2
        "Unplugging your electronics when you’re not using them could shave as much as 10 percent off your energy"
        "bill.",  # 3
        "Climate change is heating the world evenly.",  # 4
        "Climate change and extreme weather are linked.",  # 5
        "As climate warms, we will no longer have snow storms and cold days.",  # 6
        "We definitely know that tornadoes are increasing in frequency because of climate change.",
        # 7
        "All climate scientists in the 1970s were saying that we were going into an Ice Age or cooler Earth.",
        # 8
        "Growing leafy green plants is the most effective method for permanently storing carbon dioxide.",
        # 9
        "Scientists have reached common agreement and have adopted consensus-driven global policies that monitor"
        "effective, safe, reliable long-term storage of carbon dioxide.",  # 10
        "The atmosphere is composed mainly of nitrogen and oxygen.",  # 11
        "Climate change is the same thing as global warming",  # 12
        "The Earth's climate has changed before",  # 13
        "Climate change can harm plants and animals",  # 14
        "The sun causes global warming")  # 15
    answers = ("true",  # 0
               "true",  # 1,
               "false",  # 2
               "true",  # 3
               "false",  # 4
               "true",  # 5
               "false",  # 6
               "false",  # 7
               "false",  # 8
               "false",  # 9
               "false",  # 10
               "true",  # 11
               "false",  # 12
               "true",  # 13
               "true",  # 14
               "false")  # 15


    questions = list(questions)
    answers = list(answers)
    random_index_number = random.randint(0, len(questions) - 1)
    random_ques = questions[random_index_number]
    right_answer = answers[random_index_number]
    return random_ques, right_answer

@app.route('/quiz')
def quiz_game():
    question, answer = questions_answers()
    response = {
        'question': question,
        'answer': answer
    }
    print(question, answer)
    return response


#gamer input departure airport and name
@app.route('/gamerinfo')
def gamerinfo():
    args = request.args
    name = args.get('name')
    location = args.get('location')
    #print(name, location)
    sql = "INSERT into game (screen_name, location) "
    sql += "VALUES ('" + name + "','" + location + "')"
    #print(sql)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    sql2 = "SELECT * from game "
    sql2 += "WHERE id=" + str(cursor.lastrowid) +";"
    #print(sql2)
    cursor.execute(sql2)
    result = cursor.fetchone()
    ap = airport(location)
    result['airport'] = ap
    print(json.dumps(result))
    return result

#fetch airport in the city
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

@app.route('/airport/<icao>')
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


#Fetch weather condition when entering longitude and latitude of the airport

@app.route('/weather')
def weather():
    args = request.args
    latitude = args.get('lat')
    longitude = args.get('long')
    #print(longitude, latitude)
    request_link = "https://api.openweathermap.org/data/2.5/weather?lat=" + latitude + "&lon=" + longitude + "&units=metric&appid=aa8e935a3667b6a53c9bf49d4ba2904a"
    response = requests.get(request_link).json()
    #print(json.dumps(response, indent=2))
    description = response["weather"][0]["description"]
    temp = response["main"]["temp"]
    wind = response['wind']['speed']
    icon = response["weather"][0]['icon']
    jsonData = {
        'description': description,
        'temperature': temp,
        'wind': wind,
        'icon': icon
    }
    print(jsonData)
    return jsonData


@app.route('/airportdistance')
def calculate_distance_between_airports():
    args = request.args
    start_airport = fetch_airport_names_by_icao_code(args.get("start"))
    end_airport = fetch_airport_names_by_icao_code(args.get("end"))
    print(start_airport)
    print(end_airport)
    d = distance.distance((start_airport[2], start_airport[3]), (end_airport[2], end_airport[3])).km
    print(d)
    response = {
        "start": (start_airport[2], start_airport[3]),
        "end": (end_airport[2], end_airport[3]),
        "dist": d
    }
    return response

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5100)
