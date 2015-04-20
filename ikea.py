#!/usr/bin/python

import requests
import xml.etree.ElementTree as ET

AVAILBILITY_URL_TEMPLATE = 'http://www.ikea.com/ca/en/iows/catalog/availability/{}'

IKEA_STORE_VALUES = "414|boucherville:040|burlington:216|calgary:313|coquitlam:349|edmonton:256|etobicoke:039|montreal:149|north_york:004|ottawa:003|richmond:372|vaughan:249|winnipeg"
ikea_dict = {}
stores = IKEA_STORE_VALUES.split(":")

for store in stores:
	store_id, store_name = store.split("|")
	ikea_dict[store_name] = store_id

care = [
	"edmonton", 
	"calgary", 
	"ottawa",
	"coquitlam",
	"richmond"
	]

# all stores:
# care = ikea_dict.keys()

item_tuples = [
				# regulars
				('S19022530', 'Norm', 'black-brown', 'white'),
				('S59022528', 'Norm', 'black-brown', 'black'),
				('S79022532', 'Norm', 'gray       ', 'black'),
				('S39022534', 'Norm', 'gray       ', 'white'),
				# fives
				('S09022045', 'Five', 'black-brown', 'black'),
				('S39022044', 'Five', 'black-brown', 'white'),
				('S69022028', 'Five', 'gray       ', 'black'),
				('S89022032', 'Five', 'gray       ', 'white'),
				# lefts
				('S09022267', 'Left', 'black-brown', 'black'),
				('S49022270', 'Left', 'black-brown', 'white'),
				('S09022272', 'Left', 'gray       ', 'black'),
				('S69022274', 'Left', 'gray       ', 'white'),
				# rights
				('S49022492', 'Rght', 'black-brown', 'black'),
				('S09022494', 'Rght', 'black-brown', 'white'),
				('S59022496', 'Rght', 'gray       ', 'black'),
				('S19022498', 'Rght', 'gray       ', 'white'),
			]
item_availability_store = {}

for item_tuple in item_tuples:
	(item_code, shape, desktop_color, legs_color) = item_tuple
	item_availability_store[item_code] = {}
	r = requests.get(AVAILBILITY_URL_TEMPLATE.format(item_code))
	root = ET.fromstring(r.text)

	number_in_stock = None
	pad_size = 6
	bar_size = 10
	max_size = bar_size + 1

	# Availability
	for e1 in root[2]:
		store_id = e1.attrib.get('buCode')
		if not store_id:
			print "WTF!"; break

		for e2 in e1[0]:
			if e2.tag == 'availableStock':
				number_in_stock = e2.text
				item_availability_store[item_code][store_id] = number_in_stock

for store_name in care:
	store_id = ikea_dict[store_name]
	print "{} has:".format(store_name)
	for item_tuple in item_tuples:
		(item_code, shape, desktop_color, legs_color) = item_tuple
		availability_store = item_availability_store.get(item_code)
		number_in_stock = availability_store[store_id]

		bar_width = min(int(number_in_stock), bar_size)
		plus = "+" if int(number_in_stock) > bar_size else " "

		bar = "*"*bar_width + plus 
		pad = " "*(max_size - len(bar))

		print "\t{}- IN STOCK: {}{} ({}, {} top, {} legs)".format(item_code, bar, pad, shape, desktop_color, legs_color)

#import pdb; pdb.set_trace()
