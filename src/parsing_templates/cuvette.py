import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

URL='https://cuvette.tech/app/student/jobs/internships/filters?sortByDate=true'
use_saved=False

if not use_saved:
    response = requests.get(URL)
    page = response.content
else:
    with open('saved_pages/pages/cuvette.html', 'r') as f:
        page = f.read()

soup = BeautifulSoup(page, 'html.parser')

containers = soup.findAll('div', class_='StudentInternshipCard_innerContainer__3shqY')
print(page)

jobs = []

for container in containers:
    job_title_element = container.find('h3')
    job_title = job_title_element.text if job_title_element else None

    company_element = container.find('p')
    company = company_element.text if company_element else None

    info_divs = container.findAll('div', class_='StudentInternshipCard_info__1HW16')
    duration = None
    salary = None
    for div in info_divs:
        info_top = div.find('div', class_ = 'StudentInternshipCard_infoTop__3yl8o')
        if info_top and 'Duration'==info_top.text.strip():
            duration_element = div.find('div', class_='StudentInternshipCard_infoValue__E3Alf')
            duration = duration_element.text if duration_element else None
        elif info_top and 'Stipend per month' == info_top.text.strip():
            salary_element = div.find('div', class_ ='StudentInternshipCard_infoValue__E3Alf')
            salary = salary_element.text if salary_element else None

    location_element = container.find('div', class_='StudentInternshipCard_infoValue__E3Alf undefined')
    location = location_element.text if location_element else None

    link = None

    date_card = container.find('div', class_ = 'StudentInternshipCard_currentInfoLeft__1jLNL')
    date_element = date_card.find('p') if date_card else None
    date = date_element.text if date_element else None

    jobs.append({
        'title': job_title,
        'company': company,
        'salary': salary,
        'location': location,
        'duration': duration,
        'link': link,
        'date': date
    })



print(jobs)

    # Connect to the SQLite database
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