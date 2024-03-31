import requests
from bs4 import BeautifulSoup
import json

# Базова URL сторінки з цитатами
base_url = "http://quotes.toscrape.com"
next_page = "/"

# Структури даних для збереження результатів
quotes_list = []
authors_set = set()
authors_info = {}

while next_page:
    # Запит на отримання HTML сторінки
    response = requests.get(base_url + next_page)
    soup = BeautifulSoup(response.text, "html.parser")

    # Витягнення даних про цитати
    quotes = soup.find_all("div", class_="quote")
    for quote in quotes:
        text = quote.find("span", class_="text").text
        text = text.replace('“', '').replace('”', '')
        author = quote.find("small", class_="author").text
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]
        quotes_list.append({"tags": tags, "author": author, "quote": text})

        # Збір унікальних авторів
        if author not in authors_set:
            authors_set.add(author)
            author_page_link = quote.find("a")["href"]
            # Запит на сторінку автора для отримання додаткової інформації
            author_response = requests.get(base_url + author_page_link)
            author_soup = BeautifulSoup(author_response.text, "html.parser")
            born_date = author_soup.find("span", class_="author-born-date").text
            born_location = author_soup.find("span", class_="author-born-location").text
            description = author_soup.find("div", class_="author-description").text.strip()
            authors_info[author] = {"fullname": author, "born_date": born_date, "born_location": born_location,
                                    "description": description}

    # Перехід на наступну сторінку, якщо вона існує
    next_link = soup.find("li", class_="next")
    next_page = next_link.find("a")["href"] if next_link else None

# Збереження даних у файли JSON
with open("quotes.json", "w", encoding="utf-8") as f_quotes:
    json.dump(quotes_list, f_quotes, ensure_ascii=False, indent=4)

with open("authors.json", "w", encoding="utf-8") as f_authors:
    json.dump(list(authors_info.values()), f_authors, ensure_ascii=False, indent=4)
