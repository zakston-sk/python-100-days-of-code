import random


def calculate_hand(hand):
    """Calculate the total value of a hand, handling Aces (11 -> 1 if needed)."""
    total = sum(hand)
    # If total > 21 and there is an Ace, convert one Ace to 1
    if total > 21 and 11 in hand:
        # Replace one 11 with 1
        hand[hand.index(11)] = 1
        total = sum(hand)
    return total


def get_card(deck):
    """Draw a random card from the deck."""
    return random.choice(deck)


def deal_initial_hand(deck):
    """Deal two cards for a player."""
    return [get_card(deck), get_card(deck)]


def get_valid_action():
    """Ask user to hit or stand with input validation."""
    while True:
        try:
            action = int(input("Enter 0 to hit or 1 to stand: "))
            if action in (0, 1):
                return action
            print("Please enter 0 or 1.")
        except ValueError:
            print("Invalid input. Please enter a number (0 or 1).")


def play_blackjack():
    print("Welcome to the BlackJack game!")

    deck = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    while True:
        user_hand = deal_initial_hand(deck)
        computer_hand = deal_initial_hand(deck)

        user_sum = calculate_hand(user_hand)
        computer_sum = calculate_hand(computer_hand)

        print(f"Your hand: {user_hand} (Total: {user_sum})")
        print(f"Computer's first card: {computer_hand[0]}")

        # Check for player Blackjack
        if user_sum == 21:
            print("Blackjack! You win!")
        else:
            # Player's turn
            while user_sum < 21:
                action = get_valid_action()
                if action == 0:  # hit
                    card = get_card(deck)
                    user_hand.append(card)
                    user_sum = calculate_hand(user_hand)
                    print(f"Your hand: {user_hand} (Total: {user_sum})")
                else:  # stand
                    break

            # Check if player busted
            if user_sum > 21:
                print("You bust! You lose.")
            else:
                # Computer's turn (if player didn't bust)
                print(f"Computer's full hand: {computer_hand} (Total: {computer_sum})")
                while computer_sum < 17:
                    card = get_card(deck)
                    computer_hand.append(card)
                    computer_sum = calculate_hand(computer_hand)
                    print(f"Computer draws: {card} -> {computer_hand} (Total: {computer_sum})")

                # Determine winner
                if computer_sum > 21:
                    print("Computer busts! You win!")
                elif computer_sum > user_sum:
                    print("Computer wins!")
                elif computer_sum < user_sum:
                    print("You win!")
                else:
                    print("It's a draw.")

        # Ask to play again
        again = input("Play again (y/n): ").lower()
        if again != "y":
            print("Goodbye!")
            break


def main():
    play_blackjack()


if __name__ == "__main__":
    main()