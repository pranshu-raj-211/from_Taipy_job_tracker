import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

URL=''
use_saved=True

if not use_saved:
    page = requests.get(URL)
else:
    with open('saved_pages/internshala.html', 'r') as f:
        page = f.read()

soup = BeautifulSoup(page, 'html.parser')

containers = soup.findAll('div', class_='')


jobs = []
for container in containers:
    job_title = container.find()
    company = container.find()
    salary = container.find()
    location = container.find()

    duration = container.find()
    link = container.find()
    date = container.find()
    jobs.append({
        'title': job_title,
        'company': company,
        'salary': salary,
        'location': location,
        'duration': duration,
        'link': link,
        'date': date
    })

    # Connect to the SQLite database
    conn = sqlite3.connect('jobs.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create a table to store the jobs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            company TEXT,
            salary TEXT,
            location TEXT,
            duration TEXT,
            link TEXT,
            date TEXT
        )
    ''')

    # Insert the jobs into the database
    for job in jobs:
        cursor.execute('''
            INSERT INTO jobs (title, company, salary, location, duration, link, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            job['title'],
            job['company'],
            job['salary'],
            job['location'],
            job['duration'],
            job['link'],
            job['date']
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()