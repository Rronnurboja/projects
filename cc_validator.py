# 1. remove '-' or ' '
# 2. add all digits in the odd places from right to left
# 3. double every second digit from right to left
#  (if the result is a two-figit number, add it together to get a single digit)
# 4. sum the totals of steps 2 & 3
# 5. if sum is divisible by 10, the credit card is valid

# the math behind it is: from backwards, the odd-placed ordered numbers (first, third etc.) get to be added to each other,
# the even-placed ordered numbers (second etc.) get multiplied by 2 and if the result is double-digit, it adds within itself (7 * 2 =14  , 1+4=5)
# sum of odd digits should be 32 and so should the even digits

sum_odd_digits=0
sum_even_digits=0
total=0

# 1
card_number=input("Enter a credit card number: ").replace("-","").replace(" ","")
card_number = card_number[::-1] # to reverse the string

# 2  odd numbers  (index 0 to index 2 means it touches only the odd ones like 1,3 for example)
for i in card_number[::2]:  # going through every other element
    sum_odd_digits += int(i)

# 3  even numbers  (start from index 1 to 3 etc.)
for u in card_number[1::2]:
    u = int(u)*2
    if u >= 10:
        sum_even_digits += 1 + (u % 10)
    else:
        sum_even_digits += u

# 4
total = sum_even_digits + sum_odd_digits

# 5
if total % 10 == 0:
    print("VALID")
else:
    print("INVALID")
