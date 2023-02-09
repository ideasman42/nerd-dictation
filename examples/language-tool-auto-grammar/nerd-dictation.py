# This example has minimal configuration and lets Language Tool do the work to
# make it look right. (I am not at all affiliated with Language tool, I just
# found it useful to work with nerd-dictation.)
#
# Language Tool is a free service (or local server for the paranoid!) for low
# request volume and I have added it to my nerd-dictation configuration to
# correct and add punctuation where necessary.  I have found that it makes far,
# far less manual editing in the result of the spoken text:
#   https://languagetool.org/
#
# Here is a simple example:
#
# Raw spoken input:
#    can we go to costa rica in june question mark it is for my son's twelfth
#    birthday and i hope we have a lot of fun period
#
# This is the result without editing:
#    Can we go to Costa Rica in June? It is for my son's twelfth birthday and
#    I hope we have a lot of fun.
#
# For which the following rules were applied:
#    Rule: UPPERCASE_SENTENCE_START
#    Rule: EN_SPECIFIC_CASE
#    Rule: MORFOLOGIK_RULE_EN_US
#    Rule: UPPERCASE_SENTENCE_START
#    Rule: I_LOWERCASE
#
# nerd-dictation was invoked as follows:
#    ./nerd-dictation begin --config examples/language-tool/nerd-dictation.py
#
# I used the Vosk model vosk-model-en-us-0.22-lgraph, but it probably does not
# matter which model you use.

import re
import requests
from pprint import pprint

PUNCTUATION = {
    "comma": ",",
    "period": ".",
    "exclamation mark": "!",
    "question mark": "?",
}

# Change this if necessary:
language = "en-US"


def nerd_dictation_process(text):
    print("\n\n<<<< " + text)

    # Fix up punctuation first because the grammar parser works better:
    for match, replacement in PUNCTUATION.items():
        text = re.sub("\s*" + match + "(\s+|$)", lambda x: replacement + x.group(1), text)

    # Iterate langtool while it finds additional changes (or 3 tries):
    tries = 3
    while True:
        new_text = langtool(text, language)
        if new_text == text or not tries:
            break
        else:
            text = new_text

        tries -= 1

    print(">>>> " + new_text)

    return new_text


# Simple API function.  Documentation:
#    https://languagetool.org/http-api/swagger-ui/#!/default/post_check
def langtool(text, language):
    r = requests.post(
        "https://api.languagetoolplus.com/v2/check",
        data={
            "text": text,
            "language": language,
            "enabledOnly": "false",
            "level": "default",
            #'level': 'picky', # or be more picky
        },
    )

    orig_len = len(text)
    new_len = 0
    for m in r.json()["matches"]:
        # len(text) can change while iterating due to additions or deletions,
        # which breaks the offset.  Adjust the offset if length changes:
        if new_len:
            adj = new_len - orig_len
        else:
            adj = 0

        o = m["offset"] + adj
        n = m["length"]

        print("  Rule: " + m["rule"]["id"])
        if m["rule"]["id"] in ["TOO_LONG_SENTENCE"]:
            # Skip rules from Language Tool that you don't want:
            print("============== langtool skipping ID: " + m["rule"]["id"])

        elif len(m["replacements"]) >= 1:
            # Try the first replacement
            text = text[:o] + m["replacements"][0]["value"] + text[o + n :]

        elif n > 0:
            # No replacement suggestions, but a length is provided so point out
            # the unexpected content with square brackets:
            text = text[:o] + "[" + text[o : o + n + 1] + "]" + text[o + n + 1 :]

        else:
            # If we get here this is probably an unhandled case:
            print("\n\n======== langtool no replacement? " + text)

            # Limit the "replacements" list to prevent huge debug:
            m["replacements"] = m["replacements"][0:3]
            pprint(m)

        new_len = len(text)

    return text
