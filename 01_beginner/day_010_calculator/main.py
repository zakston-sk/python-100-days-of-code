import art
import calculator


VALID_OPERATIONS = "+-*/"


def get_float(prompt):
    """Prompt the user until a valid floating-point number is entered."""
    while True:
        user_input = input(prompt).strip()

        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_operation(prompt):
    """Prompt the user unitl a supported operation is entered."""
    while True:
        operation = input(prompt).strip()

        if operation and operation in VALID_OPERATIONS:
            return operation

        print(f"Invalid operation. Choose one of: {", ".join(VALID_OPERATIONS)}")


def get_next_action():
    """Ask wether to continue, start overm or quit."""
    while True:
        action = input(
            "Continue with the current result? "
            "[y = yes, n = new calculation, q = quit]: "
        ).strip().lower()

        if action in ("y", "n", "q"):
            return action

        print("Invalid input. Please enter y, n, or q.")


def perform_calculation(first_operand):
    """Perform one calculation and return its result."""
    operation = get_operation("Enter operation [+, -, *, /]: ")
    second_operand = get_float("Enter next operand: ")

    result = calculator.calculate(operation, first_operand, second_operand)

    print(f"{first_operand:g} {operation} {second_operand:g} = {result:g}")

    return result


def main():
    print(art.logo)

    while True:
        current_result = get_float("Enter first operand: ")

        while True:
            current_result = perform_calculation(current_result)
            action = get_next_action()

            if action == "y":
                continue
            elif action == "q":
                print("Goodbye!")
                return
            else:
                print()
                break


if __name__ == "__main__":
    main()