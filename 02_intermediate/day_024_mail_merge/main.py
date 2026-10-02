"""Mail Merge (Day 24).

Reads a list of names and a letter template, then generates a
personalised letter for each recipient.
"""

from pathlib import Path

INPUT_DIR = Path("./Input")
OUTPUT_DIR = Path("./Output/ReadyToSend")
NAMES_PATH = INPUT_DIR / "Names" / "invited_names.txt"
TEMPLATE_PATH = INPUT_DIR / "Letters" / "starting_letter.txt"
NAME_PLACEHOLDER = "[name]"


def read_names(path: Path) -> list[str]:
    """Return a list of non-empty names from the given file."""
    names: list[str] = []
    with path.open(encoding="utf-8") as file:
        for line in file:
            name = line.strip()
            if name:
                names.append(name)
    return names


def read_template(path: Path) -> str:
    """Return the letter template as a single string."""
    with path.open(encoding="utf-8") as file:
        return file.read()


def write_letter(path: Path, letter: str) -> None:
    """Write the given letter text to the given file."""
    path.write_text(letter, encoding="utf-8")


def build_letter(template: str, name: str) -> str:
    """Return the template with the name placeholder replaced."""
    return template.replace(NAME_PLACEHOLDER, name)


def output_path_for(name: str) -> Path:
    """Return the output file path for a given recipient name."""
    filename = name.lower().replace(" ", "_")
    return OUTPUT_DIR / f"letter_for_{filename}.txt"


def main() -> None:
    """Generate a personalised letter for every invited name."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    names = read_names(NAMES_PATH)
    template = read_template(TEMPLATE_PATH)

    for name in names:
        letter = build_letter(template, name.title())
        write_letter(output_path_for(name), letter)

    print(f"Done! Generated {len(names)} letter(s).")


if __name__ == "__main__":
    main()
