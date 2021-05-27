
#######
Hacking
#######

While contributions to this repository a welcome,
features which may be personal for your own usage should be implemented in your own user configuration.

*If unsure, open an issue with the suggestion.*


Code Base
=========

This code base is designed to be easily hacked on.

- Single file code-base (the contents of ``nerd-dictation``).
- Only built in modules are used (besides ``vosk`` for speech to text).
- So far this has only tested on Linux/X11
  *(support for other platforms may be added in the future).*


Conventions
===========

Style
-----

- Auto formatting is handled with black by running: ``black nerd-dictator``
- Ensure correct type annotations by running: ``mypy --strict nerd-dictator``.


Technical Details
=================

- All messages should be displayed via the ``sys.stderr``
  the main reason for this is it allows the text itself to be written to the ``sys.stdout``
  without other messages being mixed in.
  This works as no messages should be printed to the output when everything is working properly.

- It is important for the recording to start as soon as possible so the recording does not start
  after the user has begun speaking.
  Some operations including importing ``vosk`` are delayed for this reason.
