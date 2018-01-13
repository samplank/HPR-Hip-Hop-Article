import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import os
import re
import time
class TimeoutException(Exception): pass

with open('missed_loc_riaa4.csv', 'r') as f:
	reader = csv.reader(f)
	artists = (list(reader))[1:]

driver = webdriver.Firefox()
driver.get("https://musicbrainz.org/search?query=IT%27S+STILL+ROCK+%27N%27+ROLL+TO+ME+billy+joel&type=recording&method=indexed")

def find_link(artist):
	try:
		driver.get("https://musicbrainz.org/search?query=IT%27S+STILL+ROCK+%27N%27+ROLL+TO+ME+billy+joel&type=recording&method=indexed")
		time.sleep(3)
		search = driver.find_element_by_id('headerid-query')
		search.clear()
		search.send_keys(artist)

		time.sleep(3)

		search_but = driver.find_element_by_tag_name('button')
		search_but.click()

		time.sleep(3)

		pghtml = driver.page_source
		soup = BeautifulSoup(pghtml, "html.parser")

		rows = soup.find_all('tr')
		top_row = rows[2]
		tds = top_row.find_all('td')
		artist_td = tds[4]
		artist_link = (artist_td.find('a'))['href']
		full_link = "https://musicbrainz.org" + artist_link
		return full_link
	except:
		return None

def find_city(link):
	try:
		driver.get(link)
		time.sleep(3)
		pghtml = driver.page_source
		soup = BeautifulSoup(pghtml, "html.parser")
		try:
			genre_tab = soup.find("div", {"id": "sidebar-tags"})
			genres = genre_tab.find_all('bdi')
			genre_list = []
			for genre in genres:
				genre = genre.string
				# genre = str(genre)
				# genre_list += ' '
				# genre_list += "'"
				# genre_list += genre
				# genre_list += "'"
				genre_list.append(genre)
		except:
			genre_list = []

		try:
			begin_tab = soup.find(class_ = 'begin_area')
			areas = begin_tab.find_all('bdi')
			hometown = areas[0].string 
			area = areas[1].string

		except:
			area_tab = soup.find(class_ = 'area')
			hometown = area_tab.find('bdi').string
			area = 'no_area'

		return hometown, area, genre_list
			
	except:
		return None


writer_file = open("loc_riaadata_jun10.csv", 'a')
missed_list = open("missed_loc_riaa5.csv", 'w')
for artist in artists:
	search = artist[1] + ' ' + artist[0]
	link = find_link(search)
	area = find_city(link)
	if area != None:
		artist.append(area[0])
		artist.append(area[1])
		artist.append(area[2])
		writer_file.write(artist[0].encode('utf-8').strip() + ', ' + artist[1].encode('utf-8').strip() + ', ' + artist[2].encode('utf-8').strip() + ', ' + artist[3].encode('utf-8').strip() + ', ' + artist[4].encode('utf-8').strip() + ', ' + artist[5].encode('utf-8').strip() + ', ' + str(artist[6]) + '\n')
		writer_file.flush()
		os.fsync(writer_file.fileno())
	else:
		missed_list.write(artist[0].encode('utf-8').strip() + ', ' + artist[1].encode('utf-8').strip() + ', ' + artist[2].encode('utf-8').strip() + ', ' + artist[3].encode('utf-8').strip()+ '\n')
		missed_list.flush()
		os.fsync(missed_list.fileno())


writer_file.close()
missed_list.close()
driver.close()





