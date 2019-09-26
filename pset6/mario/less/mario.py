import cs50

while True:
    height = cs50.get_int("Height: ")
    if height > 0 and height <= 8:
        break

def draw(n):
    for i in range(n):
        for j in range(n - 1, i, -1):
            print(" ", end = "")
        for j in range(0, i + 1, 1):
            print("#", end = "")
        print("\n", end = "")

draw(height)