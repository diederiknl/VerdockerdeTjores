from flask import g
import sqlite3
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'databases', 'testgpt.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database_path)
        db.row_factory = sqlite3.Row
    return db

connection = get_db()

with open('./static/sql/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()