from cs50 import SQL
import csv
import sys

if len(sys.argv) != 2:
    exit(1)

db = SQL("sqlite:///students.db")
filename = sys.argv[1]


def sql(first, middle, last, house, year):
    sql = f"INSERT INTO students (first, middle, last, house, birth) values ('{first}', '{middle}', '{last}', '{house}', '{year}')"
    return sql


with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        name = row[0].split(' ')
        if len(name) == 2:
            name.insert(1, 'None')
        print(f"{row[0]}, born {row[2]}")
        db.execute(sql(name[0], name[1], name[2], row[1], row[2]))

