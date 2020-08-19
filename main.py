import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://www.lueftner-cruises.com/'
url = 'https://www.lueftner-cruises.com/en/river-cruises/cruise.html'


def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return r.text


def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', {'class': 'travel-box-content'})
    links = [item.find('a').get('href') for item in items]
    return links


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('div', {'class': 'cruise-headline'}).find('h1').text
    days = soup.find('p', {'class': 'cruise-duration pull-right'}).text
    itinerary = [(re.sub("^\s+|\n|\r|\s+$", '', item.text)) for item in soup.find_all('span', {'class': 'route-city'})]
    dates = [{
        item.find('span', {'class': 'price-duration'}).text: {
            'ship': item.find('span', {'class': 'table-ship-name'}).text,
            'price': item.find('span', {'class': 'big-table-font'}).text.strip()
        }}
             for item in soup.find_all('div', {'class': 'accordeon-panel-default'})]
    return {'name': name,
            'days': days,
            'itinerary': itinerary,
            'dates': dates}


if __name__ == '__main__':
    links = get_links(get_html(url))
    data = [get_content(get_html(base_url + link)) for link in links[:4]]
    print(data)