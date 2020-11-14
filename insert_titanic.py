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
# cursor.close()
CSV_FILEPATH = 'titanic.csv'

# # ## Retrieve Titanic Data ##
# df = pd.read_csv(CSV_FILEPATH)

# # Prepare Pclass column for enumeration
# df['Pclass'] = df['Pclass'].map({3:'3rd', 2:'2nd', 1:'1st'})
# # print(df.head())
# # print(df.dtypes)

## Create Postgres Titanic table & insert data ##
# Create enumerated class for Pclass

create_titanic_query = """
-- CREATE TYPE passclass AS ENUM('3rd', '2nd', '1st');
DROP TABLE IF EXISTS titanic;
CREATE TABLE IF NOT EXISTS titanic(
    id SERIAL PRIMARY KEY,
    survived BOOLEAN,
    pclass passclass,
    name TEXT,
    sex VARCHAR(6),
    age DECIMAL,
    siblings_spouses_aboard SMALLINT,
    parents_children_aboard SMALLINT,
    fare Decimal(7,4)
    );
 """
cursor.execute(create_titanic_query)

# # # Insert titanic data into Postgres Database
# # This is not the method we are learning, no schema creation
# # It creates the whole table in one step
# engine = create_engine(DB_URL)
# df.to_sql('titanic2', engine)

conn.commit()
