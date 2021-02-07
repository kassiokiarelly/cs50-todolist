import csv
import sys
import re

if len(sys.argv) != 3:
    print('Usage: python dna.py database.csv sequence.txt')
    exit(1)


databaseFilename = sys.argv[1]
sequenceFilename = sys.argv[2]

sequenceFile = open(sequenceFilename)
sequence = sequenceFile.read()


def findMaxCountSequence(strSeq):
    pattern = fr'((?:{strSeq})+)'
    rx = re.compile(pattern)
    matches = rx.findall(sequence)
    max = 0
    strLen = len(strSeq)
    for m in matches:
        count = len(m) / strLen
        if count > max:
            max = count
    return int(max)


strList = []
matchName = 'No match'
with open(databaseFilename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader, None)
    strList = header[1:]
    for row in csv_reader:
        matches = 0
        lenStr = len(strList)
        for strNum in range(lenStr):
            c = findMaxCountSequence(strList[strNum])
            isMatch = c == int(row[strNum + 1])
            if isMatch:
                matches += 1
            else:
                break
        if matches == len(strList):
            matchName = row[0]
            break


print(matchName)