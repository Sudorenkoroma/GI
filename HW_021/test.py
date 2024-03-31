from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

uri = "mongodb+srv://sudorenkoroma:sudorenkoroma@cluster0.vcn7idw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.db02.cats

# Send a ping to confirm a successful connection
# try:
#     db.cats.insert_one({
#         "name": 'barsik',
#         "age": 3,
#         "features": ['ходить в капці', 'дає себе гладити', 'рудий'],
#     })
#     print("Successfuly")
# except Exception as e:
#     print(e)

# result_many = db.cats.insert_many(
#     [
#         {
#             "name": "Lama",
#             "age": 2,
#             "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
#         },
#         {
#             "name": "Liza",
#             "age": 4,
#             "features": ["ходить в лоток", "дає себе гладити", "білий"],
#         },
#     ]
# )
# print(result_many.inserted_ids)

# db = client.db02
#
# result = db.cats.find_one({"_id": ObjectId("65fc4e0fc945d7c040e5bb52")})
# print(result)

def read_all_cats():
    try:
        cats = db.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"An error occurred: {e}")

read_all_cats()