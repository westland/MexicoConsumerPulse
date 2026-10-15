import sqlite3
conn = sqlite3.connect('data/mexico_consumer_insights.db')
c = conn.cursor()
c.execute('UPDATE consumer_problems SET city = ? WHERE city LIKE ?', ('Mérida & Yucatán', '%rida%'))
conn.commit()
conn.close()
print('Done')