REPORT = "report"
OFF = "off"

ESPRESSO = "espresso"
LATTE = "latte"
CAPPUCCINO = "cappuccino"

MENU = {
    ESPRESSO: {
        "ingredients": {"water": 50, "coffee": 18},
        "cost": 1.5,
    },
    LATTE: {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 2.5,
    },
    CAPPUCCINO: {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 3.0,
    },
}

resources = {
    "water": 850,
    "milk": 500,
    "coffee": 150,
    "money": 0.0,
}


def check_resources(ingredients):
    """Check if there are enough resources to make the drink."""
    for ingredient, amount in ingredients.items():
        if resources[ingredient] < amount:
            print(f"Sorry there is not enough {ingredient}.")
            return False
    return True


def get_integer(prompt):
    """Prompt the user for a valid integer."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Oops! That was no valid number. Try again...")


def process_coins(cost):
    """Prompt for coins and check if the inserted amount is enough."""
    print("Please insert coins.")
    quarters = get_integer("How many quarters?: ")
    dimes = get_integer("How many dimes?: ")
    nickles = get_integer("How many nickles?: ")
    pennies = get_integer("How many pennies?: ")
    total = quarters * 0.25 + dimes * 0.1 + nickles * 0.05 + pennies * 0.01

    if total < cost:
        print("Sorry that's not enough money. Money refunded.")
        return False

    change = total - cost
    if change > 0:
        print(f"Here is ${change:.2f} in change.")
    return True


def make_coffee(coffee_name):
    """Prepare the chosen coffee if resources and payment are sufficient."""
    if coffee_name not in MENU:
        return

    coffee = MENU[coffee_name]

    if not check_resources(coffee["ingredients"]):
        return

    if not process_coins(coffee["cost"]):
        return

    for ingredient, amount in coffee["ingredients"].items():
        resources[ingredient] -= amount

    resources["money"] += coffee["cost"]
    print(f"Here is your {coffee_name}. Enjoy!")


def print_resources():
    """Print the current resource report."""
    print(f"Water:   {resources['water']}ml")
    print(f"Milk:    {resources['milk']}ml")
    print(f"Coffee:  {resources['coffee']}g")
    print(f"Money:  ${resources['money']:.2f}")


def main():
    """Run the coffee machine."""
    running = True
    while running:
        user_input = input(
            f"What would you like? ({ESPRESSO}/{LATTE}/{CAPPUCCINO}): "
        ).strip().lower()

        if user_input in (ESPRESSO, LATTE, CAPPUCCINO):
            make_coffee(user_input)
        elif user_input == REPORT:
            print_resources()
        elif user_input == OFF:
            print("Turning off...")
            print("Goodbye!")
            running = False
        else:
            print("Invalid input! Try one more time.")


if __name__ == "__main__":
    main()
