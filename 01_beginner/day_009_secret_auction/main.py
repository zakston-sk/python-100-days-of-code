import logo


print(logo.logo)

bids = {}
running = True

while running:
    name = input("What is your name?: ")
    bid = int(input("What is your bid?: $"))
    bids[name] = bid
    restart = input("Are there any other bidders? Type 'yes' or 'no': ").lower()
    running = restart == 'yes'
    print("\n" * 100)

highest_bid = 0
winner = ""

for name in bids:
    if bids[name] > highest_bid:
        highest_bid = bids[name]
        winner = name

print(f"The winner is {winner} with a bid of ${highest_bid}")
