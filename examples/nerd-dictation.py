# User configuration file typically located at `~/.config/nerd-dictation/nerd-dictation.py`
import re


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
# Ignore Words
WORD_IGNORE = [
    "huh",
]


# -----------------------------------------------------------------------------
# Main Processing Function

def nerd_dictation_process(text):
    #if all words in WORD_IGNOR are found in text, return None
    if all(word in text for word in WORD_IGNORE):
        return None
    #remove all words in text that are in WORD_IGNORE
    text = re.sub(r"\b(%s)\b" % "|".join(WORD_IGNORE), "", text)

    for match, replacement in TEXT_REPLACE_REGEX:
        text = match.sub(replacement, text)

    words = text.split(" ")

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

    return " ".join(words)
