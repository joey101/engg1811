# This will be following the tutorial from https://realpython.com/beautiful-soup-web-scraper-python/
# as an introduction to webscraping and starting the journey.

# Imports the library that helps scrape and request for HTML elements of the 
# website.
import requests
from bs4 import BeautifulSoup

# The URL to be scraped.
URL = "https://realpython.github.io/fake-jobs/"

# Requests data from the "server" i.e the URL
page = requests.get(URL)
# Testing 
#print(page.text)

# Takes html content as input. (used .content instead of .text in order to get
# raw bytes)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")

job_elements = results.find_all("div", class_="card-content")

for i in job_elements:
    print(i.find("h2", class_="title"))
