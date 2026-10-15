import sqlite3

conn = sqlite3.connect('data/mexico_consumer_insights.db')
c = conn.cursor()
proper_name = "M\u00e9rida & Yucat\u00e1n"
c.execute("UPDATE consumer_problems SET city = ? WHERE city LIKE '%rida%'", (proper_name,))
c.execute("UPDATE daily_reports SET report_title = 'M\u00e9rida & Yucat\u00e1n Regional Consumer Intelligence Briefing - 2026-10-14' WHERE report_date LIKE '%merida%'")
conn.commit()

c.execute("SELECT DISTINCT city FROM consumer_problems")
print("Cities in DB:", [r[0] for r in c.fetchall()])
conn.close()
