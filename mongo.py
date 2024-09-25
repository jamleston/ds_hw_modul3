from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

# connecting to compass

client = MongoClient(
    "mongodb+srv://user:12345@cluster0.mxpz2.mongodb.net/",
    server_api=ServerApi('1')
)

# creating database

db = client.book

# adding items

result_one = db.cats.insert_one(
    {
        "name": "barsik",
        "age": 3,
        "features": ["ходить в капці", "дає себе гладити", "рудий"],
    }
)

result_many = db.cats.insert_many(
    [
        {
            "name": "Lama",
            "age": 2,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
    ]
)
