import requests
from bs4 import BeautifulSoup
import json
import re
all_items = []
link_list = []
url = 'https://index.minfin.com.ua/ua/russian-invading/casualties'
link_list.append(url)

def scrape_casualties_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    losses_data = {}

    for day in soup.find_all('li', class_='gold'):
        date = day.find('span', class_='black').text.strip()
        daily_data = {}
        casualties_div = day.find('div', class_='casualties')
        if not casualties_div:
            print(f"No casualties data found for {date}")
            continue

        for item in casualties_div.find_all('li'):
            try:
                key, value = item.text.split("—")
                value = re.search("\d+", value).group()
                key = key.strip()
                daily_data[key] = value
            except (IndexError, ValueError) as e:
                print(f"Error processing item '{item.text}': {e}")

        losses_data[date] = daily_data

    all_items.append(losses_data)


response = requests.get(url + "/")
soup = BeautifulSoup(response.content, "html.parser")
next_page = soup.select('div[class=ajaxmonth] h4[class=normal] a')
for month in next_page:
    month = re.search("(\d{4})-(\d{2})", month['href']).group()
    new_link = url + "/" + month
    link_list.append(new_link)

for day_to_scrap in link_list:
    scrape_casualties_data(day_to_scrap)



with open('casualties_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_items, f, ensure_ascii=False, indent=4)

print("Data has been successfully extracted and saved to 'casualties_data.json'.")
