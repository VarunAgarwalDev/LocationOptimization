import tensorflow as tf
import pandas as pd
import csv

class Business:

	def __init__(self, lat, lng, is_business):
		self.lat = lat
		self.lng = lng
		self.is_business = is_business

	def get_dict(self):
		return {'latitude': self.lat, 'longitude': self.lng, 'is_business': self.is_business}

def read_data():
	
	data = pd.read_csv('business_type.csv')
	data_dict = data.to_dict()

	latitude_dict = data_dict['latitudeCrd']
	longitude_dict = data_dict['longitudeCrd']
	business_dict = data_dict['commercialPropertyTypeDsc']

	businesses = []

	for index in latitude_dict:

		if latitude_dict[index] > 38.8091362319 and latitude_dict[index] < 38.9540637681 and longitude_dict[index] < -77.0185362319 and longitude_dict[index] > -77.1634637681:

			business_bool = 0;

			if business_dict[index] == 'General Commercial':
				business_bool = 1

			curr_business = Business(latitude_dict[index], longitude_dict[index], business_bool)
			businesses.append(curr_business)

	write_to_csv(businesses)

def write_to_csv(businesses):

	f = open('businesses.csv', 'w')
	fieldnames = ['latitude', 'longitude', 'is_business']
	writer = csv.DictWriter(f, fieldnames)

	writer.writeheader()

	for elem in businesses:
		writer.writerow(elem.get_dict())

	f.close()

def create_tensors():

	filename_queue = tf.train.string_input_producer(['businesses.csv'])

	reader = tf.TextLineReader()
	key, value = reader.read(filename_queue)

	record_defaults = [[0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]]

	col1, col2, col3, col4, col5, col6, col7, col8 = tf.decode_csv(value, record_defaults=record_defaults)
	features = tf.pack([col1, col2, col3, col4])

	with tf.Session() as sess:
		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(coord=coord)

		for i in range(10):
			example, label = sess.run([features, col5, col6, col7, col8])

	coord.request_stop()
	coord.join(threads)

# Categorical base columns

# Type of business (bar/casino)

# Continous base columns

# Distance from nearby ATMs
# Number of crimes in the area
# Foot traffic in the area
