from bs4 import BeautifulSoup
import requests
import sqlite3
import csv
import html

conn = sqlite3.connect("job_postings.db")
cur = conn.cursor()
cur.execute('''drop table if exists job_postings''')
cur.execute('''CREATE TABLE "job_postings" ("title"	TEXT, "link" TEXT, "employer" TEXT);
            ''')

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/84.0'
}

brightermonday = "https://www.brightermonday.co.ke/jobs"
myjobsinkenya = "https://www.myjobsinkenya.com/"
brighterresponse = requests.get(brightermonday, headers)
jobsinkenyaresponse = requests.get(myjobsinkenya, headers)
brightercontent = BeautifulSoup(brighterresponse.content, "html.parser")
jobsinkenyacontent = BeautifulSoup(jobsinkenyaresponse.content, "html.parser")

brighter_postings = brightercontent.findAll('article', attrs={"class": "search-result"})
jobsinke_postings = jobsinkenyacontent.findAll('div', attrs={"class": "content"})
job_posting = []

for posting in brighter_postings:
    try:
        title = posting.find('h3').text
    except AttributeError:
        continue
    link = posting.find('a').get('href')
    employer = html.unescape(posting.find('div', attrs={"class": "search-result__job-meta"}).text)

    brighterjob_post = {
        "title": posting.find('h3').text,
        "link": posting.find('a').get('href'),
        "employer": posting.find('div', attrs={"class": "search-result__job-meta"}).text,
    }
    job_posting.append(brighterjob_post)

    # output to csv
    with open('./combined.csv', 'a', newline='') as post:
        post_csv = csv.writer(post)
        post_csv.writerow([title, link, employer])

    # output to database
    ## replaced '' with "" in the values so as to allow for words with apostrophe eg L'Alberto
    conn.execute(f'''
    insert into job_postings (title, link, employer)
    values("{title}", '{link}', "{employer}")
    ''')

for posting in jobsinke_postings:
    title = posting.find('h4').text
    link = "https://www.myjobsinkenya.com/" + posting.find('a').get('href')
    employer = posting.find('span', attrs={"class": "company"}).text

    jobsinkejob_post = {
        "title": posting.find('h4').text,
        "link": "https://www.myjobsinkenya.com/" + posting.find('a').get('href'),
        "employer": posting.find('span', attrs={"class": "company"}).text,
    }
    job_posting.append(jobsinkejob_post)

    # output to text
    filename = './combined.txt'
    with open(filename, 'w+') as file_object:
        file_object.write(str(job_posting))
    # append to csv
    with open('./combined.csv', 'a+', newline='') as post:
        post_csv = csv.writer(post)
        post_csv.writerow([title, link, employer])

    # append output to database
    conn.execute(f'''
    insert into job_postings (title, link, employer)
    values("{title}", '{link}', "{employer}")    
    ''')

conn.commit()

conn.close()
