import requests
import time
from bs4 import BeautifulSoup as BS
from handlers.menu import TaskHandler
from handlers.bot import send_notify

def get_ctypro_rank(coins):
	result = {}
	url = requests.get('https://coinranking.com/ru').text
	soup = BS(url, 'lxml')

	all_rows = soup.find_all('tr', class_='table__row--click')

	for row in all_rows:
		ticker = row.find('span', class_='profile__subtitle-name')

		if ticker:
			ticker.text.strip().lower()

			if ticker in coins:
				price = row.find('td', class_='table__cell--responsive')

				if price:
					price = int(float(price.find("div", class_="valuta--light").text\
								.replace("$", "").replace(",", ".").replace(" ", "")\
								.replace("\n", "").replace("\xa0", "")))
				result[ticker.lower()] = price
	return result

def check_coins_balance():
	while True:
		coins = TaskHandler.read_task_file()
		coin_dict = get_ctypro_rank(coins.keys())

		for name, price in coins.items():
			if name in coin_dict:
				if coin_dict[name] <= int(price):
					send_notify(f'[{name}] - buy\nprice: {coin_dict[name]}')
					TaskHandler.delete_task_in_file(name, update=False)

		time.sleep(10)
			
