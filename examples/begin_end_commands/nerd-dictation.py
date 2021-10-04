# User configuration file typically located at `~/.config/nerd-dictation/nerd-dictation.py`

# This examples shows how explicit start/end commands can be implemented.
#
# This assumes dictation is always running in the background,
# special commands are spoken to start/end dictation which are excluded

# Global, track when dictation is active.
is_active = False

# -----------------------------------------------------------------------------
# Constants

# Commands to use.
START_COMMAND = ("start", "dictation")
FINISH_COMMAND = ("finish", "dictation")


# -----------------------------------------------------------------------------
# Utility Functions

def match_words_at_index(haystack_words, haystack_index, needle_words):
    """
    Check needle_words is in haystack_words at haystack_index.
    """
    return (
        (needle_words[0] == haystack_words[haystack_index]) and
        (haystack_index + len(needle_words) <= len(haystack_words)) and
        (needle_words[1:] == haystack_words[haystack_index + 1 : haystack_index + len(needle_words)])
    )


# -----------------------------------------------------------------------------
# Main Processing Function

def nerd_dictation_process(text):
    global is_active

    words_input = tuple(text.split(" "))
    words = []

    i = 0

    # First check if there is text prior to having begun/ended dictation.
    # The part should always be ignored.
    if is_active:
        while i < len(words_input):
            if match_words_at_index(words_input, i, START_COMMAND):
                i += len(START_COMMAND)
                break
            i += 1
        if i == len(words_input):
            i = 0
        # Else keep the advance of 'i', since it skips text before dictation started.

    while i < len(words_input):
        word = words_input[i]
        if is_active:
            if match_words_at_index(words_input, i, FINISH_COMMAND):
                is_active = False
                i += len(FINISH_COMMAND)
                continue
        else:
            if match_words_at_index(words_input, i, START_COMMAND):
                is_active = True
                i += len(START_COMMAND)
                continue

        if is_active:
            words.append(word)
        i += 1

    return " ".join(words)
