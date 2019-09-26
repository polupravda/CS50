import cs50
import sys

if not len(sys.argv) == 2:
    print("Usage: python vigenere.py key")
    sys.exit(1)

k = sys.argv[1]
if not k.isalpha():
    print("Enter a string")
    sys.exit(1)

for kk in k:
    kk = ord(kk.lower()) - ord('a')

p = cs50.get_string("plaintext: ")
count = 0
print("ciphertext: ", end="")
for pp in p:
    key = (ord(k[(count % len(k))].lower()) - ord('a'))
    if pp.isalpha() and pp.islower():
        c = chr((((ord(pp) - ord('a')) + key) % 26) + ord('a'))
        count += 1
        print(c, end = "")
    elif pp.isalpha() and pp.isupper():
        c = chr((((ord(pp) - ord('A')) + key) % 26) + ord('A'))
        count += 1
        print(c, end = "")
    else:
        c = pp
        print(c, end = "")
print()