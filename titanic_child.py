"""Creating a table about the children on the Titanic"""
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

query3 = """
SELECT
	pclass,
	sex,
    survived,
    COUNT(name)
FROM titanic
WHERE age < 18
GROUP BY pclass, sex, survived
ORDER BY pclass, sex, survived
"""
result3 = cursor.execute(query3)
result3 = cursor.fetchall()

df_child = pd.DataFrame(result3, columns=['pclass', 'sex', 'survived', 'number'])
print(df_child)

conn.close