# This will be following the tutorial from https://realpython.com/beautiful-soup-web-scraper-python/
# as an introduction to webscraping and starting the journey.

# Imports the library that helps scrape and request for HTML elements of the 
# website.
import requests
from bs4 import BeautifulSoup

# The URL to be scraped.
URL = "https://pythonjobs.github.io/"

#Requests data from the "server" i.e the URL
page = requests.get(URL)
# Testing 
#print(page.text)

# Takes html content as input. (used .content instead of .text in order to get
# raw bytes)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("section", class_="job_list")
#print(results.text)

job_elements = results.find_all("div", class_="job")
# print(job_elements)
count = 1
for i in job_elements:
    # Finds the HTML class/elemnt that we want to read, then strips it to just 
    # the words on the screen. h2 = the type of title
    job_title = i.find("h1")
    
    print(str(count)+ ".", job_title.text.strip())
    count += 1
