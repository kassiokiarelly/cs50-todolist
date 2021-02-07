from cs50 import get_string

text = get_string("Text: ")
countLetters = 0
countWords = 0
countSentences = 0

finalSentence = [".", "?", "!"]

actualChar = 0
textLength = len(text)
for char in text:
    actualChar += 1
    if char.isalpha():
        countLetters += 1
    elif char == " ":
        countWords += 1
    elif char in finalSentence:
        countSentences += 1
        if actualChar == textLength:
            countWords += 1


l = (countLetters * 100) / countWords
s = (countSentences * 100) / countWords
index = (0.0588 * l) - (0.296 * s) - 15.8

if index > 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {index:.0f}")
