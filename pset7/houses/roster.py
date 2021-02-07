from cs50 import SQL
import csv
import sys

if len(sys.argv) != 2:
    exit(1)

db = SQL("sqlite:///students.db")
house = sys.argv[1]

result = db.execute(f"select * from students where house = '{house}' order by last, first")
for r in result:
    middle = ""
    if r['middle'] != 'None':
        middle = f" {r['middle']}"
    print(f"{r['first']}{middle} {r['last']}, born {r['birth']}")

