import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_url(position, location):# 
	# Generate a url from position and location
	template = "https://nl.indeed.com/jobs?q={}&l={}"
	url = template.format(position, location)
	return url


def get_record(card):
	#extracting job data from a dingle record
	job_title = card.find('h2', 'jobTitle', 'title').text.strip()
	job_summary = card.find('div', 'job-snippet').text.strip()

	record = (job_title, job_summary)

	return record


def main(position, location):
	#Runs the main program
	records = []
	url = get_url(position, location)

	while True:
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		cards = soup.find_all('div', 'slider_container')

		for card in cards:
			record = get_record(card)
			records.append(record)

		try:
			url = 'https://nl.indeed.com' + soup.find('a', {'aria-label': 'Volgende'}).get('href') #clicks next page
		except AttributeError:
			break

	# saving the data
	with open('results.csv', 'w', newline='', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(['job_title', 'job_summary'])
		writer.writerows(records)

main('junior data engineer', 'Nederland') #example to run the program