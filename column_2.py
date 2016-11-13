import csv
import pandas as pd
from urllib.request import urlopen
import json
import sys
from math import sqrt

class Location:

	def __init__(self, lat, lng):
		self.lat = lat
		self.lng = lng

	def distance(self, other):

		return sqrt(pow((self.lat - other.lat), 2) + pow((self.lng - other.lng), 2))

	def __repr__(self):

		return 'Latitude: ' + str(self.lat) + ' Longitude: ' + str(self.lng)

def read_data():

	data = pd.read_csv('test_points.csv')
	data_dict = data.to_dict()

	lat_dict = data_dict['latitude']
	lng_dict = data_dict['longitude']

	locations = []

	for index in lat_dict:

		curr_location = Location(lat_dict[index], lng_dict[index])
		locations.append(curr_location)

	return locations

def create_distances_array():

	locations_array = read_data()
	atm_array = []

	for elem in ATM.atm_list:

		curr_location = Location(elem.lat, elem.lng)
		atm_array.append(curr_location)

	smallest_distances = []

	for location in locations_array:

		min_distance = sys.maxsize

		for atm in atm_array:

			if location.distance(atm) < min_distance:

				min_distance = location.distance(atm)

		smallest_distances.append(min_distance)

	f = open('column_2.csv', 'w')
	fieldnames = ['distance']
	writer = csv.DictWriter(f, fieldnames)

	writer.writeheader()

	for elem in smallest_distances:
		writer.writerow({'distance': elem})

	f.close()

class ATM:

	atm_list = []

	def __init__(self, atmID, name, lng, lat, access, amount, languages):
		
		self.atmID = atmID
		self.name = name
		self.lng = lng
		self.lat = lat
		self.access = access
		self.amount = amount
		self.languages = languages

	def __lt__(self, other):

		if self.amount < other.amount:
			return True
		
		return False

	def __str__(self):

		return 'ATM ID: ' + self.atmID + '\nName: ' + self.name + '\nLongitude: ' + str(self.lng) + '\nLatitude: ' + str(self.lat) + '\nAccessibility: ' + str(self.access) + '\nAmount: ' + str(self.amount) + '\nLanguages: ' + str(self.languages) + '\n\n'

def json_to_dict(url):
	
	html = urlopen(url)
	json_string = html.read()

	parsed_json = json.loads(json_string.decode())
	parseData(parsed_json)

def parseData(json_dict):

	for atm in json_dict['data']:

		curr_atm = ATM(atm['_id'], atm['name'], atm['geocode']['lng'], atm['geocode']['lat'], atm['accessibility'], atm['amount_left'], atm['language_list'])
		ATM.atm_list.append(curr_atm)

	if 'next' in json_dict['paging']:

		front = 'http://api.reimaginebanking.com'
		back = json_dict['paging']['next']

		concatenated_url = front + back
		json_to_dict(concatenated_url)
