# This will be following the tutorial from https://realpython.com/beautiful-soup-web-scraper-python/
# as an introduction to webscraping and starting the journey.

# Imports the library that helps scrape and request for HTML elements of the 
# website.
import requests
from bs4 import BeautifulSoup

# The URL to be scraped.
URL = "https://au.indeed.com/jobs?q=robotics+engineer"

#Requests data from the "server" i.e the URL
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)   Gecko/20100101 Firefox/78.0", 
"Referer": "https://www.google.com"}

page = requests.get(URL, headers=headers)

# Testing 
print(page.status_code)

# Takes html content as input. (used .content instead of .text in order to get

soup = BeautifulSoup(page.content, "html.parser")
#print(soup.prettify())
results = soup.find('a')
print(results)
"""

job_elements = results.find_all("ul", class_="jobsearch-ResultsList")
print(job_elements)

count = 1
for i in job_elements:
    # Finds the HTML class/elemnt that we want to read, then strips it to just 
    # the words on the screen. h2 = the type of title
    job_title = i.find("h1")
    
    print(str(count)+ ".", job_title.text.strip())
    count += 1
"""
