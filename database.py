import sqlite3
import json

connection = sqlite3.connect("daycare.db")

print("Database connected!")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS dogs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    breed TEXT,
    age INTEGER,
    age_unit TEXT,
    behavior TEXT
)
""")

with open("dogs.json", "r") as file:
    dogs = json.load(file)

for name, info in dogs.items():
    cursor.execute("""
        INSERT INTO dogs (name, breed, age, age_unit, behavior)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS(
            SELECT 1 FROM dogs WHERE LOWER (name) = LOWER(?)
        )
    """, (
        name,
        info["breed"],
        info["age"],
        info["age_unit"],
        info["behavior"],
        name
    ))             

connection.commit()

cursor.execute("SELECT * FROM dogs")

print(cursor.fetchall())

connection.close()