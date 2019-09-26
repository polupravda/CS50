from cs50 import get_string
from sys import argv
import sys
import os.path


def main():

    if not len(sys.argv) == 2:
        print("Error: enter password hash")
        sys.exit(1)

    try:
        with open(argv[1], "r") as file:
            dictWords = file.readlines()
    except IOError:
        sys.exit(f"{argv[1]} does not exist")

    for i in range(len(dictWords)):
        dictWords[i] = dictWords[i].strip()

    while True:
        inputText = input("Plaintext: ")
        if inputText:
            break

    inputTextList = inputText.split()

    for t in range(len(inputTextList)):
        for i in dictWords:
            if inputTextList[t].lower() == i.lower():
                inputTextList[t] = "*" * len(inputTextList[t])

    print(" ".join(inputTextList))

if __name__ == "__main__":
    main()
