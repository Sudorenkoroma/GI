from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://sudorenkoroma:sudorenkoroma@cluster0.vcn7idw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["HW_Module_3"]
authors_db = db["authors"]
quotes_db = db["quotes"]

with open("quotes.json", "r", encoding="utf-8") as quotes_json:
    quotes = json.load(quotes_json)
    try:
        quotes_db.insert_many(quotes)
        print("quotes successfuly upload")
    except Exception as e:
        print(e)

with open("authors.json", "r", encoding="utf-8") as authors_json:
    authors = json.load(authors_json)
    try:
        authors_db.insert_many(authors)
        print("authors successfuly upload")
    except Exception as e:
        print(e)
