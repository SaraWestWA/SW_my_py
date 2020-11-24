import json
import pandas as pd
import sqlite3

conn = sqlite3.connect('rpg_db.sqlite3')
print(conn)

cursor = conn.cursor()

# query1 = """
# SELECT * FROM armory_item;
# """
# result = cursor.execute(query1).fetchall()
# print(result)

df = pd.read_sql('SELECT * FROM armory_item', con=conn)
print(df.head())

armory_item = df.to_dict(orient='records')
armory_item

res = cat_facts.insert_many(cat_fact_data_transformed)