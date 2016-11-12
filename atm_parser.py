from urllib.request import urlopen
import json

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


