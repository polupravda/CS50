import cs50
import sys

if not len(sys.argv) == 2:
    print("Usage: python caesar.py key")
    sys.exit(1)

if int(sys.argv[1]) < 0:
    print("Enter positive integer")
    sys.exit(1)

p = cs50.get_string("plaintext: ")
k = int(sys.argv[1])
print("ciphertext: ", end="")
for pp in p:
    if pp.islower():
        a = chr((((ord(pp) - ord('a')) + k) % 26) + ord('a'))
        print(a, end="")
    elif pp.isupper():
        a = chr((((ord(pp) - ord('A')) + k) % 26) + ord('A'))
        print(a, end="")
    else:
        print(pp, end="")
print()