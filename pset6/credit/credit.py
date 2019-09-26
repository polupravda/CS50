import cs50

while True:
    input = cs50.get_int("Number: ")
    if input > 0:
        break

i = input
itCount = 0
oddSum = 0
evenSum = 0
totalSum = 0

while i:
    digit = i % 10
    i = i // 10
    itCount += 1

    # if iteration is odd
    if itCount % 2 == 1:
        oddSum += digit
    # if iteration is even
    else:
        digit = digit * 2
        if digit > 9:
            digitT = digit % 10
            digit = digitT + 1
        evenSum += digit

totalSum = oddSum + evenSum

if totalSum % 10 == 0:
    # AMEX\n 34 or 37; 15-digit; # VISA\n 4; 13- and 16-digit; MASTERCARD\n 51, 52, 53, 54, or 55; 16-digit;
    if len(str(input)) == 15 and (str(input)[0] == "3" and (str(input)[1] == "4" or str(input)[1] == "7")):
        print("AMEX")
    elif len(str(input)) == 16 and (str(input)[0] == "5" and (str(input)[1] == "1" or str(input)[1] == "2" or str(input)[1] == "3" or str(input)[1] == "4" or str(input)[1] == "5")):
        print("MASTERCARD")
    elif (len(str(input)) == 13 or len(str(input)) == 16) and str(input)[0] == "4":
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")