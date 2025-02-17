# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.

1, 2, 3, 4, 5, 6, 7, 8, 9, 10

# 3, 5, 6, 9

multiples_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
final_list = []

def multiple(x):
  if(x%3 == 0):
    print(f"{x} is multiple of 3")
    return x
  elif(x%5 == 0):
    print(f"{x} is multiple of 5")
    return x
  else:
    print("multiple of neither")
    return 0

for x in multiples_list:
  if multiple(x) != 0:
    final_list.append(x)

print(final_list)

# iterate through 1000 and create a list of multiples of three and five and put them into their own lists. sum this list