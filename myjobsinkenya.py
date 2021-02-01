#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/84.0'
    }

url = "https://www.myjobsinkenya.com/"
response = requests.get(url, headers, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

job_posting = []
for posting in content.findAll('div', attrs={"class": "content"}):
    job_post = {
        "title": posting.find('h4').text,
        "link": "https://www.myjobsinkenya.com/" + posting.find('a').get('href'),
        "employer": posting.find('span', attrs={"class": "company"}).text,
        "location": posting.find('span', attrs={"class": "office-location"}).text,
        }
    job_posting.append(job_post)

    filename = './myjobsinkenya.txt'
with open(filename, 'w') as file_object:
    file_object.write(str(job_posting))
