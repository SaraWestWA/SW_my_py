import pandas as pd
import sqlite3


df = pd.read_csv('buddymove_holidayiq.csv', header=0, names=['User_Id', 'Sports',
                  'Religious', 'Nature', 'Theatre', 'Shopping', 'Picnic'])
# print(df.shape)
# print(df.describe())

# Set up connection, will create empty db
conn = sqlite3.connect('review.sqlite3')

#import data to db, replace if it already exists
df.to_sql('review', con=conn, if_exists='replace', index=False)

#create cursor
cursor = conn.cursor()

query1 = """
--- Find total number of rows
SELECT 
COUNT(DISTINCT User_Id)
FROM review; 
"""
result = cursor.execute(query1).fetchall()
print('Total number of rows:', result[0][0])

query2 = """
-- How many reviewers have reviewed 100+ Nature and 100+ Shopping?
SELECT
 COUNT(DISTINCT User_Id)
FROM review r
WHERE Shopping > 99 AND Nature > 99;
"""
result = cursor.execute(query2).fetchall()
print (f'Reviewers with 100 or more reviews for both Nature & Shopping: {result[0][0]}')

query3 = """
SELECT
	AVG(Sports),
	AVG(Religious),
	AVG(Nature),
	AVG(Theatre),
	AVG(Shopping),
	AVG(Picnic)
FROM review r
"""
result = cursor.execute(query3).fetchall()
print  ('The average number of Sports reviews is: {:.2f}'.format(result[0][0]))
print  ('The average number of Religious reviews is: {:.2f}'.format(result[0][1]))
print  ('The average number of Nature reviews is: {:.2f}'.format(result[0][2]))
print  ('The average number of Theatre reviews is: {:.2f}'.format(result[0][3]))
print  ('The average number of Shopping reviews is: {:.2f}'.format(result[0][4]))
print  ('The average number of Picnic reviews is: {:.2f}'.format(result[0][5]))

conn.close()


