# User configuration file typically located at `~/.config/nerd-dictation/nerd-dictation.py`
import re
import subprocess

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
# Map Single Words To Commands

WORD_CMD_MAP = {
    "left":     ("xdotool", "click", "--clearmodifiers", "--delay", "10", "1"),
    "middle":   ("xdotool", "click", "--clearmodifiers", "--delay", "10", "2"),
    "right":    ("xdotool", "click", "--clearmodifiers", "--delay", "10", "3"),
    "backward": ("xdotool", "click", "--clearmodifiers", "--delay", "10", "4"),
    "forward":  ("xdotool", "click", "--clearmodifiers", "--delay", "10", "5"),
}


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

    for match, replacement in TEXT_REPLACE_REGEX:
        text = match.sub(replacement, text)

    words = text.split(" ")

    for i, w in enumerate(words):
        w_init = w
        cmd = WORD_CMD_MAP.get(w)
        if cmd is not None:
            subprocess.check_output(cmd).decode("utf-8")
            w = ""

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
