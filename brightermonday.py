from bs4 import BeautifulSoup
import requests
import sqlite3

conn = sqlite3.connect("output.sqlite")
cur = conn.cursor()

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/84.0'
}

url = "https://www.brightermonday.co.ke/jobs"
response = requests.get(url, headers, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

# article = content.find('article', attrs={"class": "search-result"})
# employer = article.find('div', attrs={"class": "search-result__job-meta"})
# print(article.prettify())
# print(employer.text)

job_posting = []
for posting in content.findAll('article', attrs={"class": "search-result"}):
    job_post = {
        "title": posting.find('h3').text,
        "link": posting.find('a').get('href'),
        "employer": posting.find('div', attrs={"class": "search-result__job-meta"}).text,
    }

    job_posting.append(job_post)

# writing to database

for job_post in job_posting:
    cur.execute("INSERT INTO scraped_data (title, link, employer) values (?, ?, ?)",
                (job_post["title"], job_post["link"], job_post["employer"])
                )
