"""Create PostgresSQL database, populate and query"""
import os
import pandas as pd
import psycopg2

from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load .env file and get credentials
load_dotenv()
DB_HOST = os.getenv('DB_HOST', default='OOPS')
DB_NAME = os.getenv('DB_NAME', default='OOPS')
DB_USER = os.getenv('DB_USER', default ='OOPS')
DB_PASS = os.getenv('DB_PASS', default='OOPS')
DB_URL = os.getenv('DB_URL', default='OOPS')

# Connect to ElephantSQL hosted Postgress DB
conn = psycopg2.connect(dbname=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST)

cursor = conn.cursor()
'''# Create enumerated class for Pclass
create_titanic_classes = """
--CREATE TYPE passclass AS ENUM('3rd', '2nd', '1st');
--CREATE TYPE gender AS ENUM('male', 'female');
"""
cursor.execute(create_titanic_classes)
'''
# Prepare data and create titanic database

CSV_FILEPATH = 'titanic.csv'

# ## Retrieve Titanic Data ##
column_list = ['survived', 'pclass', 'name', 'sex', 'age', 'siblings_spouses_aboard',
                'parents_children_aboard', 'fare']
df = pd.read_csv(CSV_FILEPATH, names = column_list, header=0)

# Prepare Pclass column for enumeration
df['pclass'] = df['pclass'].map({3:'3rd', 2:'2nd', 1:'1st'})
# print(df.head())

# ## Insert titanic data into Postgres Database - in one step ##
engine = create_engine(DB_URL)
df.to_sql('titanic', engine)



conn.commit()

'''This code is for creating a class with schema, not used
# create_titanic_table = """
# DROP TABLE IF EXISTS titanic;
# CREATE TABLE IF NOT EXISTS titanic(
#     id SERIAL PRIMARY KEY,
#     survived BOOLEAN,
#     pclass passclass,
#     name TEXT,
#     sex VARCHAR(6),
#     age DECIMAL,
#     siblings_spouses_aboard SMALLINT,
#     parents_children_aboard SMALLINT,
#     fare Decimal(7,4)
#     );
cursor.execute(create_titanic_table)'''
