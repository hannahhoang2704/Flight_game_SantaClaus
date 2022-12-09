import mysql.connector
import random

import requests
from geopy import distance

connection = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='game_project',
    user='root',
    password='MyN3wP4ssw0rd',  # !QAZ2wsx#EDC or MyN3wP4ssw0rd ##CHECK PASSWORD TO RUN THE PROGRAM!!!
    autocommit=True
)

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



class Airport(TransitAirport):

    route = TransitAirport()
    def __init__(self):
        self.frank = 0

    def airport_position_by_icao(self, ICAO):
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
                # print(row)
                # print(list_of_airport)
        random_nr = random.randint(0, len(list_of_airport) - 1)
        while distance.distance(list_of_deg[random_nr],
                                rovaniemi_deg).km > new_transit.calc_distance_to_Rov() or distance.distance(
                list_of_deg[random_nr],
                rovaniemi_deg).km == 0 or distance.distance(
                list_of_deg[random_nr],
                rovaniemi_deg).km == new_transit.calc_distance_to_Rov():
            random_nr = random.randint(0, len(list_of_airport) - 1)

        return list_of_airport[random_nr], list_of_deg[
            random_nr]  # random airport to transit within the range

    def get5Airport(self):
        for i in range(5):
            deg_lat = self.airport_position_by_icao(location_by_ICAO)[
                0]  # Latitude and longitude degree of departure airport
            deg_long = self.airport_position_by_icao(location_by_ICAO)[1]

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

            airport_name = \
            pick_airport(point_x_minus, point_x, point_y_minus, point_y)[
                0]  # call the transit airport
            airport_spot_deg = \
            pick_airport(point_x_minus, point_x, point_y_minus, point_y)[1]

            new_transit = Airport(airport_name, airport_spot_deg[0],
                                  airport_spot_deg[1])

            new_transit.airport_info()  # call our the airport where you are
            new_transit.weather_check()  # weather info of the transit

            route.visited_airport(airport_name,
                                  new_transit.deg)  # add the transit airport to the list
            dist_between_each_a = route.distance_between_each_airport(i + 1)
            print(
                f"You've flew {dist_between_each_a} km")  # Distance between each airport
            co2_each_transit = route.api_co2(dist_between_each_a)
            print(
                f"You've just consumed {co2_each_transit}")  # Print out the co2 consumption after moved to new transit
            print(
                f"Total consumption: {round(player1.co2_add(co2_each_transit), 2)}")  # Total amount of C02 consumption
            print(
                f"Still {new_transit.calc_distance_to_Rov():.2f} km away from Rovaniemi")  # Distance from certain transit airport to Rovaniemi
