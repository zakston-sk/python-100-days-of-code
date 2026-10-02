# Mail Merge
Reads a list of invited names and a letter template, then generates a personalised letter for each recipient.

## What I Practiced
- Reading from and writing to files with `pathlib.Path`.
- Using `with path.open(...)` so files are closed automatically.
- Replacing placeholders in a template string.
- Splitting logic into small, focused functions.
- Creating output directories safely with `mkdir(parents=True, exist_ok=True)`.

## How to Run
1. Make sure Python 3 is installed.
2. Navigate to the `day_024_mail_merge` folder.
3. Run the script:
   ```bash
   python main.py
   ```
