import logo
import alphabet


def caesar(text, shift, direction, charset):
    charset_length = len(charset)
    shifted_text = ""

    if direction == "decode":
        shift *= -1

    for character in text:
        if character in charset:
            original_index = charset.index(character)
            shifted_index = (original_index + shift) % charset_length
            shifted_text += charset[shifted_index]
        else:
            shifted_text += character

    print(f"Here is the {direction}d result: {shifted_text}")


print(logo.logo_ascii)

running = True
while running:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))

    caesar(text, shift, direction, charset=alphabet.en)

    restart = input("Type 'yes' if you want to continue. Otherwise, type 'no'.\n").lower()
    running = restart != "no"

print("Good bye!")
