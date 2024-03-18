import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

URL='https://in.indeed.com/jobs?q=machine+learning&l=Remote&from=searchOnHP'
use_saved=False
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
}

if not use_saved:
    response = requests.get(URL, headers=headers)
    page = response.content
    print(response.status_code, page)
else:
    with open('intern-tracker/cache/indeed_mar.html', 'r') as f:
        page = f.read()

soup = BeautifulSoup(page, 'html.parser')

def get_jobs(soup):
    containers = soup.findAll('div', class_='job_seen_beacon')

    jobs = []
    for container in containers:
        job_title_element = container.find('h2', class_='jobTitle css-14z7akl eu4oa1w0')
        company_element = container.find('span', {'data-testid': 'company-name'})
        salary_element = container.find('div', {'class': 'metadata salary-snippet-container css-5zy3wz eu4oa1w0'})
        location_element = container.find('div', {'data-testid': 'text-location'})
        date_element = container.find('span', {'class': 'css-qvloho eu4oa1w0'})

        job_title = job_title_element.text if job_title_element else None
        company = company_element.text if company_element else None
        salary = salary_element.text if salary_element else None
        location = location_element.text if location_element else None
        link = job_title_element.find('a')['href'] if job_title_element else None
        date = list(date_element.children)[-1] if date_element else None

        jobs.append({
            'title': job_title,
            'company': company,
            'salary': salary,
            'location': location,
            'duration':'Not specified',
            'link': link,
            'date': date
        })

# for job in jobs:
#     print(job)

    # # Connect to the SQLite database
    # conn = sqlite3.connect('jobs.db')

    # # Create a cursor object to execute SQL queries
    # cursor = conn.cursor()

    # # Create a table to store the jobs
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS jobs (
    #         id INTEGER PRIMARY KEY,
    #         title TEXT,
    #         company TEXT,
    #         salary TEXT,
    #         location TEXT,
    #         duration TEXT,
    #         link TEXT,
    #         date TEXT
    #     )
    # ''')

    # # Insert the jobs into the database
    # for job in jobs:
    #     cursor.execute('''
    #         INSERT INTO jobs (title, company, salary, location, duration, link, date)
    #         VALUES (?, ?, ?, ?, ?, ?, ?)
    #     ''', (
    #         job['title'],
    #         job['company'],
    #         job['salary'],
    #         job['location'],
    #         job['duration'],
    #         job['link'],
    #         job['date']
    #     ))

    # # Commit the changes and close the connection
    # conn.commit()
    # conn.close()