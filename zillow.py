import requests
from bs4 import BeautifulSoup
import sqlite3

def create_table():
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS listings 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  price TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def scrape_zillow():
    url = 'https://www.zillow.com/homes/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        listings = soup.select('.list-card')

        conn = sqlite3.connect('zillow_listings.db')
        c = conn.cursor()

        for listing in listings:
            property_title = listing.select_one('.list-card-info h3 a').text.strip()
            property_price = listing.select_one('.list-card-price').text.strip()

            data = {
                'title': property_title,
                'price': property_price
            }
            c.execute("INSERT INTO listings (title, price) VALUES (?, ?)", (data['title'], data['price']))
            conn.commit()
            conn.close()

if __name__ == '__main__':
    create_table()
    scrape_zillow()