from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


def main():
    menu = Menu()
    maker = CoffeeMaker()
    machine = MoneyMachine()

    running = True
    while running:
        choice = input(f"What would you like? ({menu.get_items()}): ")
        if choice == "off":
            running = False
        elif choice == "report":
            maker.report()
            machine.report()
        else:
            drink = menu.find_drink(choice)
            if drink and maker.is_resource_sufficient(drink) and machine.make_payment(drink.cost):
                maker.make_coffee(drink)


if __name__ == "__main__":
    main()
