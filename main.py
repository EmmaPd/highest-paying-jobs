import requests
import pandas as pd
from bs4 import BeautifulSoup

# Scrape the data from the first page of the website
response = requests.get("https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors")
payscale_page = response.text

soup = BeautifulSoup(payscale_page, "html.parser")
data = [row.getText() for row in soup.find_all(class_="data-table__value")]

# Scrape the data from the other pages
for page_no in range(2, 35):
    response = requests.get(f"https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{page_no}")
    payscale_page = response.text

    soup = BeautifulSoup(payscale_page, "html.parser")
    new_data = [row.getText() for row in soup.find_all(class_="data-table__value")]
    data.extend(new_data)

# Split data in sublists - one for each corresponding row
jobs_data = [data[x:x+6] for x in range(0, len(data), 6)]

# Create the dataframe
df = pd.DataFrame(jobs_data, columns=["Rank", "Major", "Degree Type", "Early Career Pay", "Mid-Career Pay", "% High Meaning"])

