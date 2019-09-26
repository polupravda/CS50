import cs50
import math

quarter = 25;
dime = 10;
nickel = 5;
penny = 1;
count = 0;

while True:
    input = cs50.get_float("Input sum: ")
    if input > 0:
        break

cents = round(input * 100)

while cents >= quarter:
    count += cents // quarter
    cents = cents % quarter

while cents >= dime:
    count += cents // dime
    cents = cents % dime

while cents >= nickel:
    count += cents // nickel
    cents = cents % nickel

while cents >= penny:
    count += cents // penny
    cents = cents % penny

print(count)