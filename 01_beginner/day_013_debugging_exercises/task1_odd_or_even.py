"""
Task 1: Debugging Odd or Even

Bug: used `=` (assignment) instead of `==` (comparison) in the if condition.
Fix: replaced `=` with `==`.
"""


def odd_or_even(number):
    if number % 2 == 0:
        return "This is an even number."
    else:
        return "This is an odd number."


print(odd_or_even(4))   # This is an even number.
print(odd_or_even(7))   # This is an odd number.
