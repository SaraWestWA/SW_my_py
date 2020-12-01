# Import rpb data from sqlite to mongdb

import os
import json
import pandas as pd
import pymongo
import sqlite3
from dotenv import load_dotenv

# Load .env file to get credentials
load_dotenv()
MONGO_USER = os.getenv('MONGO_USER', default = 'OOPS')
MONGO_PASS = os.getenv('MONGO_PASS', default = 'OOPS')
MONGO_CLUSTER = os.getenv('MONGO_CLUSTER_RPG', default = 'OOPS')

connection_uri = F'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUSTER}retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_uri)
db = client.rpg

conn = sqlite3.connect('rpg_db.sqlite3')
print(conn)
cursor = conn.cursor()

table_names = [
    'armory_item',
    'armory_weapon',
    'charactercreator_character',
    'charactercreator_character_inventory',
    'charactercreator_cleric',
    'charactercreator_fighter',
    'charactercreator_mage',
    'charactercreator_necromancer',
    'charactercreator_thief'
]

# Amazing ETL Loop
for i in range(len(table_names)):
    query = 'SELECT * FROM {}'.format(table_names[i]) # extract data
    # transform data by reading into dataframes then converting to dictionaries
    result = pd.read_sql(query, con=conn).to_dict(orient='records')
    db[table_names[i]].insert_many(result) # load data

conn.close

"""
# MULTIPLE LOOPS - What I wanted to turn in, but couldn't properly debug
table_names = [
    'armory_item',
    'armory_weapon',
    'charactercreator_character',
    'charactercreator_character_inventory',
    'charactercreator_cleric',
    'charactercreator_fighter',
    'charactercreator_mage',
    'charactercreator_necromancer',
    'charactercreator_thief'
]

# extract data
df_list = []
for t in table_names:
    query = 'SELECT * FROM {}'.format(t)
    df = pd.read_sql(query, con=conn)
    df_list.append(df)

# transform data
new_df_list = []
for d in range(len(df_list)):
    result = df_list[d].to_dict(orient='records')
    new_df_list.append(result)
print(len(new_df_list))

# load data
db_creator = []
for c in range(len(new_df_list)):
    db[table_names[c]].insert_many(new_df_list[c])

# ########

INDIVIDUAL TABLE - What I turned in because it worked
df_armory_item = pd.read_sql(('SELECT * FROM armory_item'), con=conn) # extract data
ai_result = df_armory_item.to_dict(orient='records') # transform data
armory_item = db.armory_item # create db documents
armory_item.insert_many(ai_result) # load data

#Repeat for each table to be collection
df_armory_weapon = pd.read_sql(('SELECT * FROM armory_weapon'), con=conn)
aw_result = df_armory_weapon.to_dict(orient='records')
armory_weapon = db.armory_weapon
armory_weapon.insert_many(aw_result)

df_charactercreator_character = pd.read_sql(('SELECT * FROM charactercreator_character'), con=conn)
ccc_result = df_charactercreator_character.to_dict(orient='records')
charactercreator_character = db.charactercreator_character
charactercreator_character.insert_many(ccc_result)

df_charactercreator_character_inventory = pd.read_sql(('SELECT * FROM charactercreator_character_inventory'), con=conn)
cci_result = df_charactercreator_character_inventory.to_dict(orient='records')
charactercreator_character_inventory = db.charactercreator_character_inventory
charactercreator_character_inventory.insert_many(cci_result)

df_charactercreator_cleric = pd.read_sql(('SELECT * FROM charactercreator_cleric'), con=conn)
ccl_result = df_charactercreator_cleric.to_dict(orient='records')
charactercreator_cleric = db.charactercreator_cleric
charactercreator_cleric.insert_many(ccl_result)

df_charactercreator_fighter = pd.read_sql(('SELECT * FROM charactercreator_fighter'), con=conn)
cf_result = df_charactercreator_fighter.to_dict(orient='records')
charactercreator_fighter = db.charactercreator_fighter
charactercreator_fighter.insert_many(cf_result)

df_charactercreator_mage = pd.read_sql(('SELECT * FROM charactercreator_mage'), con=conn)
cm_result = df_charactercreator_mage.to_dict(orient='records')
charactercreator_mage = db.charactercreator_mage
charactercreator_mage.insert_many(cm_result)

df_charactercreator_necromancer = pd.read_sql(('SELECT * FROM charactercreator_necromancer'), con=conn)
cn_result = df_charactercreator_necromancer.to_dict(orient='records')
charactercreator_necromancer = db.charactercreator_necromancer
charactercreator_necromancer.insert_many(cn_result)

df_charactercreator_thief = pd.read_sql(('SELECT * FROM charactercreator_thief'), con=conn)
ct_result = df_charactercreator_thief.to_dict(orient='records')
charactercreator_thief = db.charactercreator_thief
charactercreator_thief.insert_many(ct_result)
"""