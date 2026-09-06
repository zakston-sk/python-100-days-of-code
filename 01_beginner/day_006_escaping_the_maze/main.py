""" COPY AND PASTE
def turn_right():
    turn_left()
    turn_left()
    turn_left()

def find_starting_position():
    while front_is_clear():
        move()
    turn_left()

def find_goal():
    while not at_goal():
        if right_is_clear():
            turn_right()
            move()
        elif front_is_clear():
            move()
        else:
            turn_left()

find_starting_position()
find_goal()
"""
