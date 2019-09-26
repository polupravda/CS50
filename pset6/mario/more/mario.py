import cs50

while True:
    height = cs50.get_int("Height ")
    if height > 0 and height <= 8:
        break

def draw(n):
    for i in range(1, height + 1, 1):
        print(" " * (height - i), end = "")
        print("#" * i, end = "")
        print(" " * 2, end = "")
        print("#" * i, end = "")
        print()

draw(height)