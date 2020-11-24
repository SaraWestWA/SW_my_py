"""A few queries about titanic data"""
import os
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

query3 = """
-- How many females over the age of 35 overall?
SELECT
    COUNT(name) as females
FROM titanic
WHERE sex = 'female' AND age > 35;
"""

result = cursor.execute(query3)
total = cursor.fetchall()

print(f'There were {total[0][0]} women over the age of 35 traveling aboard the Titanic.')
for i in range(len(result1)):
    rate = round(100*(result1[i][1]/result2[i][1]),1)
    print(f'Of these {result1[i][1]} in {result2[i][0]} class survived, that is {rate}%.')

query4 = """
-- How many passengers survived, how many died?
SELECT
    COUNT(survived)
FROM titanic
GROUP BY survived
"""
result = cursor.execute(query4)
result4 = cursor.fetchall()

print ('---'*20)
print(f'Of the passengers on the Titanic {result4[0][0]} perished and {result4[1][0]} survived.')
print ('---'*20)

query5 = """
-- How many passengers in each class?
SELECT
    pclass,
    COUNT(pclass)
FROM
    titanic
GROUP BY
pclass
ORDER BY pclass DESC
"""

result = cursor.execute(query5)
result5 = cursor.fetchall()

print ('Passengers on the Titanic:')
for i in range(len(result5)):
    print(f'{result5[i][0]} class: {result5[i][1]}')
print ('---'*20)

query6 = """
 -- How many people survived/died by class?
SELECT
    pclass,
    COUNT(survived)
FROM titanic
WHERE survived = 1
GROUP BY pclass, survived
ORDER BY survived DESC, pclass DESC;
"""

result = cursor.execute(query6)
result6 = cursor.fetchall()

print ('Survivors from the Titanic:')
for i in range(len(result5)):
    print(f'{result6[i][0]} class: {result6[i][1]}')
print ('---'*20)

query7 = """
 -- How many people survived by class?
SELECT
    pclass,
    COUNT(survived)
FROM titanic
WHERE survived = 0
GROUP BY pclass, survived
ORDER BY survived DESC, pclass DESC;
"""

result = cursor.execute(query7)
result7 = cursor.fetchall()

print ('Titanic Deaths:')
for i in range(len(result7)):
    print(f'{result7[i][0]} class: {result7[i][1]}')
print ('---'*20)

query8 = """
-- What was the average age of people who survived?
-- What was the average age of people who died?
SELECT
    survived,
    AVG(age)
FROM titanic
GROUP BY survived
ORDER BY survived DESC;
"""

result = cursor.execute(query8)
result8 = cursor.fetchall()

print ('Average Age of Titanic Passengers by Survival:')
plist = ['Survived', 'Died']
for i in range(len(result8)):
    print(f'{plist[i]}: {round(result8[i][1],2)}')
print ('---'*20)

query9 = """
-- What was the average age  of passengers by class?
SELECT
    pclass,
    AVG(age)
FROM titanic
GROUP BY pclass
ORDER BY pclass DESC;
"""

result = cursor.execute(query9)
result9 = cursor.fetchall()

print ('Average Age of Titanic Passengers by Class:')
for i in range(len(result9)):
    print(f'{result9[i][0]} class: {round(result9[i][1],2)}')
print ('---'*20)

query11 = """
-- What was the average fare by class?
SELECT
    pclass,
    AVG(fare)
FROM titanic
GROUP BY pclass
ORDER BY pclass DESC;
"""

result = cursor.execute(query11)
result11 = cursor.fetchall()

print ('Average Fare by Class:')
for i in range(len(result11)):
    print(f'{result11[i][0]} class: {round(result11[i][1],2)}')
print ('---'*20)

query12 = """
-- What was the average fare for people who survived?
-- What was the average fare for people who died?
SELECT
    survived,
    AVG(fare)
FROM titanic
GROUP BY survived
ORDER BY survived DESC;
"""

result = cursor.execute(query12)
result12= cursor.fetchall()

print ('Average Fare by Survival:')
plist = ['Survived', 'Died']
for i in range(len(result12)):
    print(f'{plist[i]}: {round(result12[i][1],2)}')
print ('---'*20)

query13 = """
-- What was the average # of siblings/spouses aboard by class?
SELECT
    pclass,
    AVG(siblings_spouses_aboard)
FROM titanic
GROUP BY pclass
ORDER BY pclass DESC;
"""

result = cursor.execute(query13)
result13= cursor.fetchall()

print ('Average Siblings/Spouses by Class:')
for i in range(len(result13)):
    print(f'{result13[i][0]} class: {round(result13[i][1],2)}')
print ('---'*20)

query14 = """
-- What was the average # of siblings/spouses aboard by survival?
SELECT
    survived,
    AVG(siblings_spouses_aboard)
FROM titanic
GROUP BY survived
ORDER BY survived DESC;
"""

result = cursor.execute(query14)
result14= cursor.fetchall()

print ('Average Number of Siblingss/Spouses by Survival:')
plist = ['Survived', 'Died']
for i in range(len(result14)):
    print(f'{plist[i]}: {round(result14[i][1],2)}')
print ('---'*20)

query15 = """
-- What was the average # of parents/children aboard by class?
SELECT
    pclass,
    AVG(parents_children_aboard)
FROM titanic
GROUP BY pclass
ORDER BY pclass DESC;
"""

result = cursor.execute(query15)
result15= cursor.fetchall()

print ('Average Parents/Children by Class:')
for i in range(len(result15)):
    print(f'{result15[i][0]} class: {round(result15[i][1],2)}')
print ('---'*20)

query16 = """
-- What was the average # of parents/children aboard by survival?
SELECT
    survived,
    AVG(parents_children_aboard)
FROM titanic
GROUP BY survived
ORDER BY survived DESC;
"""

result = cursor.execute(query16)
result16= cursor.fetchall()

print ('Average Number of Parents/Children by Survival:')
plist = ['Survived', 'Died']
for i in range(len(result16)):
    print(f'{plist[i]}: {round(result16[i][1],2)}')
print ('---'*20)

query17 = """
-- Do any passengers on the Titanic have the same name?
SELECT
	name,
	COUNT(name)
FROM titanic
GROUP BY name
HAVING COUNT(name) > 1
"""
result = cursor.execute(query17)
result17= cursor.fetchall()
print(f'The list of passengers with the same name: {result17}')
print("""This could be more closely examined by dissecting the 'name' column.
However, that would involve a new table or dataframe.""")
conn.close