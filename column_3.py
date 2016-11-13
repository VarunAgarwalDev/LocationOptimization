import csv
import pandas as pd
from urllib.request import urlopen
import json
import sys

class Location:

	def __init__(self, lat, lng):
		self.lat = lat
		self.lng = lng

	def distance(self, other):

		return sqrt(pow((self.lat - other.lat), 2) + pow((self.lng - other.lng), 2))

	def __repr__(self):

		return 'Latitude: ' + str(self.lat) + ' Longitude: ' + str(self.lng)

def read_data(fileName, latName, lonName):

	data = pd.read_csv(fileName)
	data_dict = data.to_dict()

	lat_dict = data_dict[latName]
	lng_dict = data_dict[lonName]

	locations = []

	for index in lat_dict:

		curr_location = Location(lat_dict[index], lng_dict[index])
		locations.append(curr_location)

	return locations

def create_crime_index():
    crimeRadius = .001
    crimeIndexArray = []
    testPointLocations = read_data('test_points.csv', 'latitude', 'longitude')
    crimeLocations = read_data('crime_location.csv', 'latitudeCrd', 'longitudeCrd')

    for point in testPointLocations:
        crimeIndex = 0
        for crime in crimeLocations:
            if crime.lat < (point.lat + crimeRadius) and crime.lng < (point.lng + crimeRadius):
                crimeIndex += 1
        crimeIndexArray.append(crimeIndex)

    f = open('column_3.csv', 'w')
    fieldnames = ['crime index']
    writer = csv.DictWriter(f, fieldnames)

    writer.writeheader()

    for elem in crimeIndexArray:
        writer.writerow({'crime index': elem})

    f.close()
