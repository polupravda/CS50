import sys
import crypt
from itertools import product

# real data
strAlpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
maxLength = 5

if not len(sys.argv) == 2:
    print("Error: enter password hash")
    sys.exit(1)

passHash = sys.argv[1]

b = (passHash[0], passHash[1])
strS = ''
strS = strS.join(b)

for i in range(1, maxLength + 1):
    for a in product(strAlpha,repeat = i):
        strT = ''
        strT = strT.join(a)
        strHash = crypt.crypt(strT, strS)
        if passHash == strHash:
            print(f"Found! Password is: {strT}")
            exit(0)

print("Unable to crack")