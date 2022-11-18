import mysql.connector
import random
from geopy import distance
import time, os, sys
import pyfiglet
from art import black_jack_logo
import requests
import json
from count_down import statement
import quiz
import rock_paper_scissor
import black_jack


print(statement)                        #Countdown the days till Christmas

connection = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='game_project',
    user='root',
    password='MyN3wP4ssw0rd',  # !QAZ2wsx#EDC or MyN3wP4ssw0rd ##CHECK PASSWORD TO RUN THE PROGRAM!!!
    autocommit=True
)



# Function: check if the city exists in database
def check_city(city):
    sql = "SELECT count(*) from airport"
    sql += " WHERE municipality ='" + city + "'"
    # print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            row[0]
    return row[0]


# Function: search airports in the city
icao_suggested_list = []

def municipality_search(city):
    sql = "SELECT ident, name FROM airport"
    sql += " WHERE municipality='" + city + "'"
    # icao_list = []
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            print(f"      {row[0]}: {row[1]}")
            icao_suggested_list.append(row[0])
    return icao_suggested_list


# Function: call the airport by icao in the chosen city

def call_airport(icao):
    sql = "SELECT name FROM airport"
    sql += " WHERE ident='" + icao + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            print(f"\nYou are now in {row[0]}. Get ready for your flight!\n")
    return row[0]


# Function: call latitude degree and longitude degree of the airport by input ICAO

def airport_position_by_icao(ICAO):
    sql = "SELECT name, latitude_deg, longitude_deg from airport"
    sql += " WHERE ident='" + ICAO + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            deg = [row[1], row[2]]
            #print(deg)
    return deg


#Function: call random airport within the coordinator scope

def pick_airport(x1, x, y1, y):
    list_of_airport = []
    list_of_deg = []
    sql = "SELECT name, latitude_deg, longitude_deg FROM airport"
    sql += " WHERE latitude_deg between " + str(x1) + " and " + str(x) +\
           " and longitude_deg between " + str(y1) + " and " + str(y)
    #print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            list_of_airport.append(row[0])
            list_of_deg.append([row[1], row[2]])
            #print(row[0])
            #print(list_of_airport)
    random_nr = random.randint(0, len(list_of_airport) - 1)
    #print(list_of_airport[random_nr])
    #print(list_of_deg[random_nr])
    return list_of_airport[random_nr], list_of_deg[random_nr]                               #random airport to transit within the range


rovaniemi_deg = airport_position_by_icao("EFRO")                    #ROVANIEMI degree of latitude & longitude



class Airport:
    def __init__(self, name, latitude, longitude):
        #self.list_of_all_airport = []
        #self.icao_list= []
        #self.degree_list = []
        #self.icao = icao
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.deg = (self.latitude, self.longitude)

    def __str__(self):
        return self.name + "latitude: " + self.latitude + "longitude: " + self.longitude

    def airport_info(self):
        return print(f"You're in {self.name}\nDegree: {self.deg}")

    def calc_distance_to_Rov(self):                             #Distance from that airport to Rovaniemi
        dist = distance.distance(self.deg, rovaniemi_deg).km
        return dist

    def weather_check(self):  # API to give weather forecast
        request = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(
            self.latitude) + "&lon=" + str(
            self.longitude) + "&units=metric&appid=4f49bd07640eb084816fccedd67fdcbb"
        response = requests.get(request)
        if response.status_code == 200:
            json_response = response.json()
            # print(json.dumps(json_response, indent=2))
            description = json_response["weather"][0]["description"]
            temp = json_response["main"]["temp"]
            print(f"Weather in {self.name} is {description} with temperature of {temp} Celsius degree")


class TransitAirport:
    def __init__(self):
        #self.name = name
        #self.icao = icao
        #self.deg = deg
        self.airports_list = []
        #self.icao_list = []
        self.degree_list = []


class Player:
    def __init__(self, name, gift=100, co2_consumption=0):
        self.name = name
        self.gift = gift
        self.co2_consumption = co2_consumption

    def get_info(self):
        return print(f"Name: {self.name}\n{self.gift} gifts\nCo2_consumption: {self.co2_consumption}")

    def get_gift(self):
        nr_random = random.randint(1,5)
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
        nr_random = random.randint(6,8)
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


###############

#MAIN PROGRAM

list_of_visited_icao = []
player_name = str(input("Enter your name: "))
municipality = input('From which city you want to start your journey: ')

while check_city(municipality) == 0 or municipality.lower() == "rovaniemi":  # Player can't choose Rovaniemi as a starting point
    municipality = input("Oops! You can't fly from this city. Another city please: ")
else:
    print("\nHere are your adventure starting point options: ")
    municipality_search(municipality)

# Users choose the airport in the chosen city

icao_selection = input(
    f"You can see all the airports in your city above.\n(Enter ICAO to choose the airport you want to fly:)")

while icao_selection.upper() not in icao_suggested_list:
    print("Oops! Check again the ICAO code. You can't arrive to the airport if you don't call ICAO code correctly!")
    icao_selection = str(input('Enter ICAO code again:'))
else:
    location_by_ICAO = icao_selection.upper()                                   # ICAO of departure airport
    airport_dep_name = call_airport(icao_selection)                             # Departure airport variable
    dep_deg_lat = airport_position_by_icao(location_by_ICAO)[0]                 #Latitude and longitude degree of departure airport
    dep_deg_long = airport_position_by_icao(location_by_ICAO)[1]

    airport_dep = Airport(airport_dep_name, dep_deg_lat, dep_deg_long)            #store depature airport in class Airport
    print(airport_dep.airport_info())
    print(f"Distance from {airport_dep.name} to Rovaniemi is {airport_dep.calc_distance_to_Rov():.2f} km")

route = TransitAirport()
player1 = Player(player_name, 100, 1000)
coordinator_scope_x = rovaniemi_deg[0] - dep_deg_lat                           #calculate the coordinator(x,y) scope within depature airport and Rovaniemi airport
coordinator_scope_y = rovaniemi_deg[1] - dep_deg_long

dist_between_each_scope_x = round(coordinator_scope_x/4,4)
dist_between_each_scope_y = round(coordinator_scope_y/4,4)
#print(dist_between_each_scope_x)
#print(dist_between_each_scope_y)

route.airports_list.append(airport_dep.name)
#print(route1.airports_list)
route.degree_list.append(airport_dep.deg)
#print(route1.degree_list)


for i in range(5):                                                              #transit via 5 different airports before arrive Rovaniemi
    print(route.airports_list[i])
    point_x = route.degree_list[i][0] + dist_between_each_scope_x
    #print(point_x)
    point_y = route.degree_list[i][1] + dist_between_each_scope_y
    #print(point_y)
    pick_airport(route.degree_list[i][0], point_x, route.degree_list[i][1], point_y)

    airport_spot = pick_airport(route.degree_list[i][0], point_x, route.degree_list[i][1], point_y)[0]          #call the transit airport
    airport_spot_deg = pick_airport(route.degree_list[i][0], point_x, route.degree_list[i][1], point_y)[1]

    new_transit = Airport(airport_spot, airport_spot_deg[0], airport_spot_deg[1])

    new_transit.airport_info()   # call our the airport where you are
    new_transit.weather_check()  # weather info of the transit

    route.airports_list.append(airport_spot)
    route.degree_list.append(airport_spot_deg)
    #print(route1.airports_list)
    print(f"You are {new_transit.calc_distance_to_Rov():.2f} km away from Rovaniemi")               # Distance from certain transit airport to Rovaniemi



    #Choose the game to play in each place

    choose_game = int(input("Enter number of the game you want to play:\n1. Quiz\n2. Rock paper scissor\n3. Hang man\n4. Black Jack\n"))
    while choose_game not in range(1,5):
        choose_game = int(input("Enter number of the game you want to play:\n1. Quiz\n2. Rock paper scissor\n3. Hang man\n4. Black Jack\n"))
    else:
        if choose_game == 1:
            if quiz.questions_answers() == True:                                #Get more gift or deduct gift
                player1.get_gift()
            else:
                player1.deduct_gift()
        elif choose_game == 2:
            if rock_paper_scissor.rock_paper_scissors() == True:
                player1.get_gift()
            else:
                player1.deduct_gift()
        elif choose_game == 4:
            if black_jack.black_jack() == True:
                player1.player1.get_gift()
            else:
                player1.deduct_gift()

    player1.get_info()                      #Print out current score









