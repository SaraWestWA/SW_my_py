"""Module to run queries on rpg database"""
import pandas as pd
import sqlite3

conn = sqlite3.connect('rpg_db.sqlite3')
cursor = conn.cursor()

query1 = """
--- Find total number of characters
SELECT 
COUNT(DISTINCT character_id)
FROM charactercreator_character cc; 
"""
result = cursor.execute(query1).fetchall()
print('Total number of characters:', result[0][0])

query2 = """
-- Find total number of Mage
SELECT
    COUNT(character_ptr_id)
FROM charactercreator_mage;
"""
result = cursor.execute(query2).fetchall()
print('Total number Mage:', result[0][0])


query3 = """
-- Find total number of Necromancers, subset of Mage
SELECT
	COUNT(mage_ptr_id)
FROM charactercreator_necromancer;
"""
result = cursor.execute(query3).fetchall()
print('Total number Mage as Necromancer:', result[0][0])


query4 = """
-- Find total number of Thieves
SELECT
	COUNT(character_ptr_id)
FROM charactercreator_thief;
"""
result = cursor.execute(query4).fetchall()
print('Total number Thieves:', result[0][0])


query5 = """
-- Find total number of Clerics
SELECT
	COUNT(character_ptr_id)
FROM charactercreator_cleric;
"""
result = cursor.execute(query5).fetchall()
print('Total number Clerics:', result[0][0])


query6 = """
-- Find total number of Fighters
SELECT
	COUNT(character_ptr_id)
FROM charactercreator_fighter;
"""
result = cursor.execute(query6).fetchall()
print('Total number Fighters:', result[0][0])

query7 = """
-- Find total number of items, weapons & non-weaponns
SELECT
    items,
    weapons,
    items - weapons AS non_weapons
FROM(
    SELECT
        COUNT(DISTINCT(inv.item_id)) AS items,
        COUNT(DISTINCT(wep.item_ptr_id)) AS weapons
    FROM armory_item as inv
    LEFT JOIN armory_weapon as wep
    ON inv.item_id = wep.item_ptr_id
);
"""
result = cursor.execute(query7).fetchall()
print('Total number Items:', result[0][0])
print('Total number Weapons:', result[0][1])
print('Total number Non-Weapons:', result[0][2])

# query9 = """
# -- How many items does each character have?
# ANSWERED IN QUERY10
# SELECT
#     cc.character_id,
#     cc.name,
#     COUNT(cci.item_id) as num_items
# FROM charactercreator_character cc
# LEFT JOIN charactercreator_character_inventory cci 
# ON cc.character_id = cci.character_id 
# GROUP BY cc.character_id
# LIMIT 20
# """
# result = cursor.execute(query9).fetchall()
# print('Number of Items per Character:')
# item_df = pd.DataFrame(data=result, columns=['C ID', 'Name', 'Num Items'])
# print (item_df)
    
query10 = """
-- How many items does each character have?
-- How many weapons does each character have?
SELECT
	cc.character_id,
	cc.name,
    COUNT(cci.item_id) as num_items,
	COUNT(aw.item_ptr_id) as num_weapons
FROM charactercreator_character_inventory as cci
LEFT JOIN armory_weapon as aw
ON cci.item_id = aw.item_ptr_id

LEFT JOIN charactercreator_character AS cc
ON cci.character_id = cc.character_id
GROUP BY cci.character_id
LIMIT 20
"""
result = cursor.execute(query10).fetchall()
weapon_df = pd.DataFrame(data=result, columns = ['C ID', 'Name', 'Num_Items','Weapons'])
print('\n')
print ('Number of Items & Weapons per Character')
print(weapon_df,'\n')

query12 = '''
-- On average how many items does each character have?
-- On average how many weapons does each character have?
SELECT
    AVG(num_items),
    AVG(num_weapons)
FROM
(
    SELECT
        cc.character_id,
        cc.name,
        COUNT(cci.item_id) as num_items,
        COUNT(aw.item_ptr_id) as num_weapons
    FROM charactercreator_character_inventory as cci
    LEFT JOIN armory_weapon as aw
    ON cci.item_id = aw.item_ptr_id

    LEFT JOIN charactercreator_character AS cc
    ON cci.character_id = cc.character_id
    GROUP BY cci.character_id
);
'''
result = cursor.execute(query12).fetchall()
print('The average number of items per character is {:.3f}'.format(result[0][0]))
print('The average number of weapons per character is {:.3f}'.format(result[0][1]))


# query2b = """
# -- This attempt does not work, I had the impression from the first round that this
# -- can be accoplished in one query, the method I used is much slower than running
# -- individual queries.
# SELECT
#     mage,
#     theif,
#     cleric,
#     fighter
# FROM(
#     SELECT
# 	    COUNT(DISTINCT cm.character_ptr_id) as mage,
# 		COUNT(DISTINCT ct.character_ptr_id) as thief,
# 		COUNT(DISTINCT cl.character_ptr_id) as cleric,
# 		COUNT(DISTINCT cf.character_ptr_id) as fighter
# 	FROM charactercreator_character as cc
#          JOIN charactercreator_mage as cm
#         ON cc.character_id = cm.character_ptr_id,
        
# 	FROM cc
#          JOIN charactercreator_theif as ct
#         ON cc.character_id = ct.character_ptr_id,
        
# 	FROM cc
#          JOIN charactercreator_cleric as cl
#         ON cc.character_id = cl.character_ptr_id,
        
# 	FROM charactercreator_character as cc
#        	 JOIN charactercreator_fighter as cf
#         ON cc.character_id = cf.character_ptr_id
# )"""
# result = cursor.execute(query2b).fetchall()
# print('Characters:', result)

conn.close()
