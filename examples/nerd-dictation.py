# User configuration file typically located at `~/.config/nerd-dictation/nerd-dictation.py`
import re
import subprocess
import sys


# -----------------------------------------------------------------------------
# Map Words To Commands

DICTATION_CMD_NAME = "type"

WORD_CMD_MAP = {
    "left":     ("xdotool", "click", "--clearmodifiers", "--delay", "10", "1"),
    "middle":   ("xdotool", "click", "--clearmodifiers", "--delay", "10", "2"),
    "right":    ("xdotool", "click", "--clearmodifiers", "--delay", "10", "3"),
    "scroll": {
        "up":   ("xdotool", "click", "--clearmodifiers", "--delay", "10", "4"),
        "down": ("xdotool", "click", "--clearmodifiers", "--delay", "10", "5"),
    }
}



# -----------------------------------------------------------------------------
# Replace Multiple Words

TEXT_REPLACE_REGEX = (
    ("\\b" "data type" "\\b", "data-type"),
    ("\\b" "copy on write" "\\b", "copy-on-write"),
    ("\\b" "key word" "\\b", "keyword"),
)
TEXT_REPLACE_REGEX = tuple(
    (re.compile(match), replacement)
    for (match, replacement) in TEXT_REPLACE_REGEX
)


# -----------------------------------------------------------------------------
# Replace Single Words

# VOSK-API doesn't use capitals anywhere so they have to be explicit added in.
WORD_REPLACE = {
    "i": "I",
    "api": "API",
    "linux": "Linux",
}

# Regular expressions allow partial words to be replaced.
WORD_REPLACE_REGEX = (
    ("^i'(.*)", "I'\\1"),
)
WORD_REPLACE_REGEX = tuple(
    (re.compile(match), replacement)
    for (match, replacement) in WORD_REPLACE_REGEX
)


# -----------------------------------------------------------------------------
# Main Processing Function

def nerd_dictation_process(text):

    # # Determinate the command.
    if not nerd_dictation_process.cmd_name:
        words = text.split(" ")
        if words:
            cmd_name_test = words[0]

            # Reset if command is not recognised.
            if cmd_name_test != DICTATION_CMD_NAME and cmd_name_test not in WORD_CMD_MAP:
                sys.stderr.write("Command name '%s' not recognised\n" % cmd_name_test)
                sys.exit(1) # TODO: reset here instead!

            nerd_dictation_process.cmd_name = cmd_name_test

    # Process the command.
    if nerd_dictation_process.cmd_name == DICTATION_CMD_NAME:
        for match, replacement in TEXT_REPLACE_REGEX:
            text = match.sub(replacement, text)

        words = text.split(" ")
        del(words[0])

        for i, w in enumerate(words):
            w_init = w
            w_test = WORD_REPLACE.get(w)
            if w_test is not None:
                w = w_test

            if w_init == w:
                for match, replacement in WORD_REPLACE_REGEX:
                    w_test = match.sub(replacement, w)
                    if w_test != w:
                        w = w_test
                        break

            words[i] = w

        # Strip any words that were replaced with empty strings.
        words[:] = [w for w in words if w]

        return " ".join(words)

    else:
        words = text.split(" ")
        cmd_map = WORD_CMD_MAP
        cmd = ""
        for i, w in enumerate(words):
            cmd = cmd_map.get(w)
            if not isinstance(cmd, dict):
                if cmd is None:
                    sys.stderr.write("Command name or argument '%s' not recognised\n" % w)
                    sys.exit(1) # TODO: reset here instead!

                else:
                    subprocess.check_output(cmd).decode("utf-8")
                    sys.exit(0) # TODO: reset here instead!

                break # TODO: this break is needed if reset is done.

            cmd_map = cmd

        # Handle the case where the command was recognised, but not complete. #TODO: reprocess once all words available (store words if needed)?
        sys.stderr.write("Command '%s' is incomplete\n" % " ".join(words))
        sys.exit(1) # TODO: reset here instead!

        return "" # TODOD: an empty string leads to an error in the caller.


nerd_dictation_process.cmd_name = ""
