from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
import csv
import time  # For timestamp in filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    links_and_attractions = request.form.getlist('links_and_attractions')  # Get list of combined data

    for combined_data in links_and_attractions:
        try:
            link, total_attractions = combined_data.split(',')  # Separate link and attractions
            total_attractions = int(total_attractions)
            num_pages = (total_attractions // 30) + 1 if total_attractions % 30 else total_attractions // 30

            scraped_data = []  # Accumulate data across pages

            for page in range(1, num_pages + 1):
                url = link + "?page=" + str(page)  # Construct URL with pagination

                try:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Replace with your specific scraping logic (example):
                    for attraction in soup.find_all('div', class_='attraction'):
                        name = attraction.find('h3').text.strip()
                        # ... (other information to scrape)
                        scraped_data.append([name, ...])  # Append data

                except Exception as e:
                    return f'Error scraping page {page} of {link}: {str(e)}'

            # Generate unique filename with timestamp
            filename = f'scraped_data_{link.replace("/", "_")}_{int(time.time())}.csv'
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Attraction Name', ...])  # Add header row
                writer.writerows(scraped_data)

        except Exception as e:
            return f'Error processing combined data "{combined_data}": {str(e)}'  # Handle individual errors

    return f'Scraped data for each link with the provided number of attractions!'

if __name__ == '__main__':
    app.run(debug=True)

