from urllib.request import urlopen
import json
import csv

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

def write_to_file():

	sorted_atms = sorted(ATM.atm_list)[::-1]

	f = open('atm_list.txt', 'w')

	for elem in sorted_atms:

		f.write(str(elem))

	f.close()

def write_top_20():

	sorted_atms = sorted(ATM.atm_list)[::-1]

	f = open('atm_top_20.csv', 'w')
	fieldnames = ['latitude', 'longitude']
	writer = csv.DictWriter(f, fieldnames)

	writer.writeheader()

	for elem in sorted_atms[0:20]:
		writer.writerow({'latitude': elem.lat, 'longitude': elem.lng})

	f.close()



