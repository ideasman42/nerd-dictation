# This example showcases how to use nerd-dictation with a reduced grammar set.
#
# A lexicon graph is a feature built into Vosk which allows you to define the
# words and phrases that will be recognized be the speech engine. By reducing
# the grammar to a specific set of words or commands, recognition becomes
# almost 100% accurate.
#
# This is the command that I used to invoke nerd-dictation for development and
# testing of the grammar code and this example:
#
#  ./nerd-dictation begin   \
#      --continuous         \
#      --numbers-as-digits  \
#      --numbers-no-suffix  \
#      --vosk-model-dir     ~/.config/nerd-dictation/vosk-model-en-us-0.22-lgraph/ \
#      --vosk-grammar-file  ./examples/vosk_grammar/vosk-grammar.json              \
#      --config             ./examples/vosk_grammar/nerd-dictation.py
#
# = Notes about the files indicated above
#
# --vosk-model-dir vosk-model-en-us-0.22-lgraph
#
#     According to Alpha Cephei, you must have a voice model with the lexicon
#     graph. For this example I used vosk-model-en-us-0.22-lgraph which works
#     quite well.  (https://alphacephei.com/nsh/2020/03/27/lookahead.html)
#
#
# --vosk-grammar-file ./examples/vosk_grammar/vosk-grammar.json
#
#     The JSON file provided to Vosk is literal next. No python code can be
#     included their comment it is passed directly to the engine which was
#     written in C.  The special term "[unk]" will be matched if Vosk detected
#     audio but no match was found.
#
#      After loading this example, open a terminal and try speaking the following text:
#
#         cd slash e t tab enter
#         grep root pass back tab enter
#         up
#         pipe cut dash f 1 comma 6 comma 7 space dash d colon enter
#
#      On a UNIX system this should produce the following output:
#         ~]$ cd /etc/
#
#         etc]$ grep root passwd
#         root:x:0:0:root:/root:/bin/bash
#         operator:x:11:0:operator:/root:/sbin/nologin
#
#         etc]$ grep root passwd|cut -f1,6,7 -d:
#         root:/root:/bin/bash
#         operator:/root:/sbin/nologin
#
# Now see how fast you can speak and still get an accurate result!  I was
# surprised that I could speak faster than the interpreter, and perhaps even
# dictate commands faster than I can type!
#
# Of course this is a trivial example and could be extended to be far more
# featureful, but of course that is an exercise for the reader . . .

import re

NOSPACE_WORDS = {
    # Punctuation
    "slash": "/",
    "pipe": "|",
    "dash": "-",
    "colon": ":",
    "comma": ",",
    # Whitespace:
    "space": " ",
    "backspace": chr(8),
    "back": chr(8),
    "tab": "\t",
    "enter": "\r",
    # Navigation (VT102 codes)
    "up": "\x1a\x1b[A",
    "down": "\x1a\x1b[B",
    "right": "\x1a\x1b[C",
    "left": "\x1a\x1b[D",
    "home": "\x1a\x1b[1~",
    "end": "\x1a\x1bOF",
    "delete": "\x1a\x1b[3~",
}


def nerd_dictation_process(text):
    print(">> " + text)

    text = re.sub(r"^\s+|\s+$", "", text)
    text = re.sub(r"\s+", " ", text)

    words = text.split(" ")
    try:
        words.remove("[unk]")
    except:
        None

    for i, w in enumerate(words):
        x = NOSPACE_WORDS.get(w)
        if x is not None:
            words[i] = x
        elif len(w) == 1:
            # Type single letters without spaces.
            continue
        else:
            words[i] = w + " "

    return "".join(words)
