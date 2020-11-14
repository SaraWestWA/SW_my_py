"""Create PostgresSQL database, populate and query"""
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

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

# Alter pclass & gender to enumerated types
alter_class_types = """
ALTER TABLE titanic
ALTER COLUMN pclass TYPE passclass
USING pclass::passclass,
ALTER COLUMN sex TYPE gender
USING sex::gender;
"""
cursor.execute(alter_class_types)

query1 = """
-- How  many females over age 35 survived by class?
SELECT
    pclass,
    COUNT(pclass) as female_survivors
FROM titanic
WHERE survived = 1 AND sex = 'female' AND age > 35
GROUP BY pclass;
"""
result = cursor.execute(query1)
result1 = cursor.fetchall()
for i in range(len(result1)):
    print(f'Number of surviving {result1[i][0]} class females over age 35: {result1[i][1]}')

query2 = """
-- How  many female passengers were over age 35 by class?
SELECT
    pclass,
    COUNT(pclass) as females
FROM titanic
WHERE sex = 'female' AND age > 35
GROUP BY pclass;
"""
result = cursor.execute(query2)
result2 = cursor.fetchall()
for i in range(len(result2)):
    print(f'Total number of {result2[i][0]} class females over age 35: {result2[i][1]}')

for i in range(len(result2)):
    print(f'The probablity of a {result2[i][0]} class female over age 35 surviving is: {(result1[i][1]/result2[i][1]):.2}')

conn.close