"""
Task 3: Debugging FizzBuzz

Bugs:
1. Used `or` instead of `and` for the FizzBuzz condition.
2. Used `if` instead of `elif`, causing multiple prints per number.
3. Printed `[number]` (a list) instead of just `number`.
Fix: corrected the logic and used `elif` / `else`.
"""


def fizz_buzz(target):
    for number in range(1, target + 1):
        if number % 3 == 0 and number % 5 == 0:
            print("FizzBuzz")
        elif number % 3 == 0:
            print("Fizz")
        elif number % 5 == 0:
            print("Buzz")
        else:
            print(number)


fizz_buzz(15)
