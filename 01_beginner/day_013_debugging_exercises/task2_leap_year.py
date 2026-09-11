"""
Task 2: Debugging Leap Year

Bug: the year was divided by 4000 instead of 400.
Fix: changed `year % 4000` to `year % 400`.
"""


def is_leap(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


print(is_leap(2000))  # True
print(is_leap(1900))  # False
print(is_leap(2024))  # True
