import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import pandas as pd

url = "https://journeynorth.org/sightings/querylist.html?season=&map=monarch-egg-fall&year=2018&submit=View+Data"
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')  # Adjust this if necessary

    # Extract the rows from the table
    rows = table.find_all('tr')

    # Collect data in a list for sorting
    data_list = []

    # Write data rows
    for row in rows[1:]:
        columns = row.find_all('td')
        if len(columns) > 6:  # Check if there are enough columns
            state = columns[3].text.strip()  # Adjust based on actual table structure
            try:
                eggs = int(columns[6].text.strip())  # Convert to integer
                data_list.append([state, eggs])
            except ValueError:
                continue  # Skip rows with invalid number formats

    # Sort data by state
    data_list.sort(key=lambda x: x[0])  # Sort by state name

    # Open a CSV file to write the sorted data
    with open('egg2018.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header
        headers = ["State/Province", "Number of eggs"]
        writer.writerow(headers)

        # Write sorted data rows
        writer.writerows(data_list)

    print("Data has been successfully scraped and saved to 'egg2018.csv'.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

data = pd.read_csv('egg2018.csv')

plt.figure(figsize=(12, 6))
plt.bar(data['State/Province'], data['Number of eggs'], color='blue')
plt.xlabel("States")
plt.ylabel("Total Number of Eggs")
plt.title('Total Number of Monarch Eggs by State in 2018')
plt.xticks(rotation=45, ha='right')  # Rotate x labels for better visibility
plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels

plt.show()
