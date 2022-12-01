import mysql.connector
import random
from geopy import distance
import time, os, sys
import pyfiglet
import requests
import json
from count_down import statement
from quiz import questions_answers
from rock_paper_scissor import rock_paper_scissors
from black_jack import black_jack


print(statement)  # Countdown the days till Christmas

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='game_project',
    user='root',
    password='!QAZ2wsx#EDC',  # !QAZ2wsx#EDC or MyN3wP4ssw0rd ##CHECK PASSWORD TO RUN THE PROGRAM!!!
    autocommit=True
)


# Function: check if the city exists in database
def check_city(city):
    sql = "SELECT count(*) from airport"
    sql += " WHERE municipality ='" + city + "'"
    #print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
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
            print(f"\nYou are now in {row[0]}.")
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
            # print(deg)
    return deg


rovaniemi_deg = airport_position_by_icao("EFRO")  ###############ROVANIEMI degree of latitude & longitude


# Function: call random airport within the coordinator scope

def pick_airport(x1, x, y1, y):
    list_of_airport = []
    list_of_deg = []
    sql = "SELECT name, latitude_deg, longitude_deg FROM airport"
    sql += " WHERE latitude_deg between " + str(x1) + " and " + str(x) + \
           " and longitude_deg between " + str(y1) + " and " + str(y)
    # print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            list_of_airport.append(row[0])
            list_of_deg.append([row[1], row[2]])
            #print(row)
            # print(list_of_airport)
    random_nr = random.randint(0, len(list_of_airport) - 1)
    while distance.distance(list_of_deg[random_nr], rovaniemi_deg).km > new_transit.calc_distance_to_Rov() or distance.distance(list_of_deg[random_nr], rovaniemi_deg).km == 0 or distance.distance(list_of_deg[random_nr], rovaniemi_deg).km == new_transit.calc_distance_to_Rov():
        random_nr = random.randint(0, len(list_of_airport) - 1)

    return list_of_airport[random_nr], list_of_deg[random_nr]  # random airport to transit within the range


class Airport:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.deg = (self.latitude, self.longitude)

    def __str__(self):
        return self.name + "latitude: " + self.latitude + "longitude: " + self.longitude

    def airport_info(self):
        return print(f"You're in {self.name}\nDegree: {self.deg}")

    def calc_distance_to_Rov(self):  # Distance from that airport to Rovaniemi
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
        self.airports_list = []
        self.degree_list = []

    def visited_airport(self, name, deg):
        self.airports_list.append(name)
        self.degree_list.append(deg)
        return

    def distance_between_each_airport(self, index: int):
        d = round(distance.distance(self.degree_list[index], self.degree_list[index - 1]).km, 2)
        return d

    def api_co2(self, d):
        convert = d * 1.852
        f = f"https://despouy.ca/flight-fuel-api/q/?aircraft=60006b&distance={convert}"
        response = requests.get(f).json()
        amount = round(response[0]['co2'], 2)
        return amount


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


##############################################################################

# MAIN PROGRAM

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
    location_by_ICAO = icao_selection.upper()  # ICAO of departure airport
    airport_dep_name = call_airport(icao_selection)  # Departure airport variable
    dep_deg_lat = airport_position_by_icao(location_by_ICAO)[0]  # Latitude and longitude degree of departure airport
    dep_deg_long = airport_position_by_icao(location_by_ICAO)[1]

    airport_dep = Airport(airport_dep_name, dep_deg_lat, dep_deg_long)  # store depature airport in class Airport
    print(airport_dep.airport_info())
    print(f"Distance from {airport_dep.name} to Rovaniemi is {airport_dep.calc_distance_to_Rov():.2f} km")

route = TransitAirport()
player1 = Player(player_name)
new_transit = airport_dep
route.visited_airport(airport_dep.name, airport_dep.deg)  # add departure airport to the list

for i in range(5):
    deg_lat = airport_position_by_icao(location_by_ICAO)[0]  # Latitude and longitude degree of departure airport
    deg_long = airport_position_by_icao(location_by_ICAO)[1]

    coordinator_scope_x = rovaniemi_deg[
                              0] - deg_lat  # calculate the coordinator(x,y) scope within depature airport and Rovaniemi airport
    coordinator_scope_y = rovaniemi_deg[1] - deg_long

    dist_between_each_scope_x = round(coordinator_scope_x / 3, 4)
    dist_between_each_scope_y = round(coordinator_scope_y / 3, 4)

    ##transit via 5 different airports to play game and collect gift

    # transit via 5 different airports before arrive Rovaniemi
    print(route.airports_list[i])
    if dist_between_each_scope_x > dist_between_each_scope_y:
        dist_between_each_scope = dist_between_each_scope_x
    else:
        dist_between_each_scope = dist_between_each_scope_y

    point_x = route.degree_list[i][0] + dist_between_each_scope
    point_y = route.degree_list[i][1] + dist_between_each_scope

    point_x_minus = route.degree_list[i][0] - dist_between_each_scope
    point_y_minus = route.degree_list[i][1] - dist_between_each_scope

    pick_airport(point_x_minus, point_x, point_y_minus, point_y)

    airport_name = pick_airport(point_x_minus, point_x, point_y_minus, point_y)[0]  # call the transit airport
    airport_spot_deg = pick_airport(point_x_minus, point_x, point_y_minus, point_y)[1]

    new_transit = Airport(airport_name, airport_spot_deg[0], airport_spot_deg[1])

    new_transit.airport_info()  # call our the airport where you are
    new_transit.weather_check()  # weather info of the transit

    route.visited_airport(airport_name, new_transit.deg)  # add the transit airport to the list
    dist_between_each_a = route.distance_between_each_airport(i + 1)
    print(f"You've flew {dist_between_each_a} km")  # Distance between each airport
    co2_each_transit = route.api_co2(dist_between_each_a)
    print(f"You've just consumed {co2_each_transit}")  # Print out the co2 consumption after moved to new transit
    print(f"Total consumption: {round(player1.co2_add(co2_each_transit), 2)}")  # Total amount of C02 consumption
    print(
        f"Still {new_transit.calc_distance_to_Rov():.2f} km away from Rovaniemi")  # Distance from certain transit airport to Rovaniemi

    # Player chooses the game to play in every stop

    choose_game = int(
        input("Enter number of the game you want to play:\n1. Quiz\n2. Rock paper scissor\n3. Black Jack\n\n"))
    while choose_game not in range(1, 5):
        choose_game = int(
            input("Enter number of the game you want to play:\n1. Quiz\n2. Rock paper scissor\n3. Black Jack\n\n"))
    else:
        if choose_game == 1:
            if questions_answers() == True:  # Get more gift or deduct gift
                player1.get_gift()
            else:
                player1.deduct_gift()
        elif choose_game == 2:
            if rock_paper_scissors() == True:
                player1.get_gift()
            else:
                player1.deduct_gift()
        elif choose_game == 3:
            if black_jack() == True:
                player1.get_gift()
            else:
                player1.deduct_gift()

    player1.get_info()  # Print out current score
    if player1.gift > 100000000000:  # The game stop when player can't collect and more gift to continue the trip
        print("Oops! Mission incompleted!")
        break
    # print(route.airports_list)
    # print(route.degree_list)

##Game ends and player arrive the Rovaniemi airport

rov_name = call_airport("EFRO")
route.visited_airport(rov_name, rovaniemi_deg)  # Add Rovaniemi airport to the visted airport list
last_transit_to_rov = route.distance_between_each_airport(len(route.airports_list) - 1)
co2_period = route.api_co2(last_transit_to_rov)
print(f"You've just consumed {round(co2_period, 2)}")
player1.co2_add(co2_period)
player1.get_info()
