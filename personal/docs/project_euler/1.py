# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.

def main():
  def multiple(x):
    if(x%3 == 0):
      # print(f"{x} is multiple of 3")
      return True
    elif(x%5 == 0):
      # print(f"{x} is multiple of 5")
      return True
    else:
      # print("multiple of neither")
      return False

  final_list = []

  for x in range(3, 1000):
    if multiple(x):
      final_list.append(x)

  return sum(final_list)

print(main())
# iterate through 1000 and create a list of multiples of three and five and put them into their own lists. sum this list