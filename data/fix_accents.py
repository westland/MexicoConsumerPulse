import sqlite3

conn = sqlite3.connect('data/mexico_consumer_insights.db')
c = conn.cursor()
c.execute("UPDATE consumer_problems SET city = 'Mérida & Yucatán' WHERE city LIKE '%rida%'")
c.execute("UPDATE daily_reports SET report_title = 'Mérida & Yucatán Regional Consumer Intelligence Briefing - 2026-10-14' WHERE report_date LIKE '%merida%'")
conn.commit()

c.execute('SELECT DISTINCT city FROM consumer_problems')
print('Updated cities:', [r[0] for r in c.fetchall()])
conn.close()
