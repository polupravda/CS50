nums = [x for x in range(10)]
nums.append(5)
nums.insert(11, 6)
nums[len(nums):] = [7]
print(f"{nums}")

data = [
    ("elena", 1986),
    ("olya", 1992),
    ("jury", 1985)
]
for name, year in data:
    # print(f"{name} was born in {year}")
    print("{0} was born in {1}".format(name, year))

fruits = {
    "bananas": 1.09,
    "apples": 2.99,
    "oranges": 1.30
}

for fruit in fruits:
    print(fruit)

for fruit, price in fruits.items():
    print(price)

# if __name__ == "__main__":
#     main()

def square(x):
    return x * x

print(square(2))

class Student():

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def changeID(self, id):
        self.id = id

    def print(self):
        print("{} - {}".format(self.name, self.id))

elena = Student("Elena", 111)
elena.print()
elena.changeID(222)
elena.print()