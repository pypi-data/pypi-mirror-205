# built in
import json

# package
from .commandline import RED, YELLOW, ANSI_RESET


def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    # if config.json file is missing
    except FileNotFoundError:
        # print error message
        print(
            RED
            + "ERROR: Failed to find your `config.json` file in the current directory."
            + YELLOW
            + "\n\nFor help and usage instructions, see: "
            + ANSI_RESET
            + "https://gitlab.com/DrTexx/csv-transaction-history-detective/#getting-started"
        )
        # return non-zero exit code
        exit(1)
