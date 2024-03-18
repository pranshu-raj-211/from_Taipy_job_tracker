import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

URL = "https://www.ycombinator.com/jobs/role"
use_saved = False
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
}

if not use_saved:
    response = requests.get(URL, headers=headers)
    page = response.content
else:
    with open("saved_pages/yc.html", "r") as f:
        page = f.read()

soup = BeautifulSoup(page, "html.parser")

print(response.text)

containers = soup.findAll(
    "div",
    class_="mb-1 flex flex-col flex-nowrap items-center justify-between gap-y-2 md:flex-row md:gap-y-0",
)


jobs = []
for container in containers:
    job_title_element = container.find("a", class_="font-semibold text-linkColor")

    if job_title_element:
        job_title = job_title_element.text
        link = job_title_element.href

    company_element = container.find("span", class_="block font-bold md:inline")
    if company_element:
        company = company_element.text

    location_element = container.find(
        "div",
        class_="border-r border-gray-300 px-2 first-of-type:pl-0 last-of-type:border-none last-of-type:pr-0",
    )
    if location_element:
        location = location_element.text

    date_posted_element = container.find('span', class_='hidden text-sm text-gray-400 md:inline')
    if date_posted_element:
        date_posted = date_posted_element.text.strip().split('(')[1].split(')')[0]
    jobs.append(
        {
            "title": job_title,
            "company": company,
            "location": location,
            "link": link,
            "date": date_posted,
        }
    )


for job in jobs:
    print(job)
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
    #         link TEXT,
    #         date TEXT
    #     )
    # ''')

    # # Insert the jobs into the database
    # for job in jobs:
    #     cursor.execute('''
    #         INSERT INTO jobs (title, company, salary, location, link, date)
    #         VALUES (?, ?, ?, ?, ?, ?, ?)
    #     ''', (
    #         job['title'],
    #         job['company'],
    #         job['salary'],
    #         job['location'],
    #         job['link'],
    #         job['date_posted']
    #     ))

    # # Commit the changes and close the connection
    # conn.commit()
    # conn.close()
