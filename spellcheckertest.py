from spellchecker import SpellChecker

spell = SpellChecker()
input = input("Enter the text: ")

isCorrect = input in spell

if isCorrect:
    print("Dit is een woord in het Engels")
else:
    print("Dit is geen woord in het Engels")
