import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import re
import time
import datetime
class TimeoutException(Exception): pass

# writer_file = open("riaadata.csv", "w")
# writer_file.write("artist, album, level, date \n")

writer_file = open("riaa_may29.csv", "a")


driver = webdriver.Firefox()

now = datetime.datetime.now()

start_time = datetime.datetime.strptime('Aug 02 2004', '%b %d %Y')
start_time_1 = start_time + datetime.timedelta(days=1)
print(start_time)

while start_time < now:
	start = start_time.strftime("%Y-%m-%d")
	start_1 = start_time_1.strftime("%Y-%m-%d")

	page = "http://www.riaa.com/gold-platinum/?tab_active=default-award&ar=&ti=&lab=&genre=&format=&date_option=certification&from=" + start + "&to=" + start_1 + "&award=&type=&category=&adv=SEARCH#search_section"

	driver.get(page)

	time.sleep(2)

	artists = []
	songs = []
	medals = []
	dates = []

	driver.set_window_size(480, 320)
	driver.maximize_window()

	details = driver.find_elements_by_xpath("//div[@class = 'format_details']/a")
	for detail in details:
		detail.click()

	time.sleep(3)

	pghtml = driver.page_source

	soup = BeautifulSoup(pghtml, "html.parser")

	awards = soup.find_all("td", class_ = "artists_cell")
	for award in awards:
		artst = award.string
		artist = artst.lower()
		if ('&' or 'feat.') in artist:
			mult_artists = [x.strip() for x in artist.split('&')]
			mult_artists = [x.strip() for x in mult_artists[0].split('feat.')]
			artist = str(mult_artists[0])
			artist = artist.replace(',','')

		artists.append(artist)

	titles = soup.find_all(class_ = "table_award_row expanded")
	for title in titles:
		name = title.contents[5].string
		songs.append(name)

	cals = soup.find_all("span", class_ = "upper_style")
	for cal in cals:
		cal.span.decompose()
		date = cal.string
		date = date.replace(',','')
		dates.append(date)

	icy = soup.find_all("img", class_ = "award")
	medal_hold = []
	for ice in icy:
		med = str(ice['src'])
		med1 = list(med)
		med2 = list(filter(str.isdigit, med1))
		med3 = ''.join(med2)
		try:
			medal_hold.append(med3)
		except:
			pass

	del medal_hold[::2]

	if len(medal_hold) > 30:
		print('too many' + start)

	medals += medal_hold

	print(start_time)
	start_time = start_time_1
	start_time_1 = start_time + datetime.timedelta(days=1)

	artist_award = zip(artists, songs, medals, dates)

	for tup in artist_award:
		value = tup[0].encode('utf-8') + ', ' + tup[1].encode('utf-8') + ', ' + tup[2].encode('utf-8') + ', ' + tup[3].encode('utf-8') + '\n'
		writer_file.write(value)

writer_file.close
driver.close()


