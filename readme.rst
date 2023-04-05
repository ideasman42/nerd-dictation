##############
Nerd Dictation
##############

*Offline Speech to Text for Desktop Linux.* - See `demo video <https://www.youtube.com/watch?v=T7sR-4DFhpQ>`__.

This is a utility that provides simple access speech to text for using in Linux
without being tied to a desktop environment, using the excellent `VOSK-API <https://github.com/alphacep/vosk-api>`__.

Simple
   This is a single file Python script with minimal dependencies.
Hackable
   User configuration lets you manipulate text using Python string operations.
Zero Overhead
   As this relies on manual activation there are no background processes.

Dictation is accessed manually with begin/end commands.


Usage
=====

It is suggested to bind begin/end/cancel to shortcut keys.

.. code-block:: sh

   nerd-dictation begin

.. code-block:: sh

   nerd-dictation end


For details on how this can be used, see:
``nerd-dictation --help`` and ``nerd-dictation begin --help``.


Features
========

Specific features include:

Numbers as Digits
   Optional conversion from numbers to digits.

   So ``Three million five hundred and sixty second`` becomes ``3,000,562nd``.

   A series of numbers (such as reciting a phone number) is also supported.

   So ``Two four six eight`` becomes ``2,468``.

Time Out
   Optionally end speech to text early when no speech is detected for a given number of seconds.
   (without an explicit call to ``end`` which is otherwise required).

Output Type
   Output can simulate keystroke events (default) or simply print to the standard output.

User Configuration Script
   User configuration is just a Python script which can be used to manipulate text using Python's full feature set.

Suspend/Resume
   Initial load time can be an issue for users on slower systems or with some of the larger language-models,
   in this case suspend/resume can be useful.
   While suspended all data is kept in memory and the process is stopped.
   Audio recording is stopped and restarted on resume.

See ``nerd-dictation begin --help`` for details on how to access these options.


Dependencies
============

- Python 3.6 (or newer).
- The VOSK-API.
- An audio recording utility (``parec`` by default).
- An input simulation utility (``xdotool`` by default).


Audio Recording Utilities
-------------------------

You may select one of the following tools.

- ``parec`` command for recording from pulse-audio.
- ``sox`` command as alternative, see the guide: `Using sox with nerd-dictation <readme-sox.rst>`_.


Input Simulation Utilities
--------------------------

You may select one of the following input simulation utilities.

- `xdotool <https://github.com/jordansissel/xdotool>`__ command to simulate input in X11.
- `ydotool <https://github.com/ReimuNotMoe/ydotool>`__ command to simulate input anywhere (X11/Wayland/TTYs).
  See the setup guide: `Using ydotool with nerd-dictation <readme-ydotool.rst>`_.
- `dotool <https://git.sr.ht/~geb/dotool>`__ command to simulate input anywhere (X11/Wayland/TTYs).
- `wtype <https://github.com/atx/wtype>`__ to simulate input in Wayland".


Install
=======

.. code-block:: sh

   pip3 install vosk
   git clone https://github.com/ideasman42/nerd-dictation.git
   cd nerd-dictation
   wget https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip
   unzip vosk-model-small-en-us-0.15.zip
   mv vosk-model-small-en-us-0.15 model

To test dictation:

.. code-block:: sh

   ./nerd-dictation begin --vosk-model-dir=./model &
   # Start speaking.
   ./nerd-dictation end


- Reminder that it's up to you to bind begin/end/cancel to actions you can easily access (typically key shortcuts).
- To avoid having to pass the ``--vosk-model-dir`` argument, copy the model to the default path:

  .. code-block:: sh

     mkdir -p ~/.config/nerd-dictation
     mv ./model ~/.config/nerd-dictation

.. hint::

   Once this is working properly you may wish to download one of the larger language models for more accurate dictation.
   They are available `here <https://alphacephei.com/vosk/models>`__.


If you prefer to use a package, see: `Packaging <package/readme.rst>`_.


Configuration
=============

This is an example of a trivial configuration file which simply makes the input text uppercase.

.. code-block:: python

   # ~/.config/nerd-dictation/nerd-dictation.py
   def nerd_dictation_process(text):
       return text.upper()


A more comprehensive configuration is included in the ``examples/`` directory.

Hints
-----

- The processing function can be used to implement your own actions using keywords of your choice.
  Simply return a blank string if you have implemented your own text handling.

- Context sensitive actions can be implemented using command line utilities to access the active window.


Paths
=====

Local Configuration
   ``~/.config/nerd-dictation/nerd-dictation.py``
Language Model
   ``~/.config/nerd-dictation/model``

   Note that ``--vosk-model-dir=PATH`` can be used to override the default.


Command Line Arguments
======================

.. BEGIN HELP TEXT

Output of ``nerd-dictation --help``

usage::

       nerd-dictation [-h]  ...

This is a utility that activates speech to text on Linux.
While it could use any system currently it uses the VOSK-API.

positional arguments:

    :begin:               Begin dictation.
    :end:                 End dictation.
    :cancel:              Cancel dictation.
    :suspend:             Suspend the dictation process.
    :resume:              Resume the dictation process.

options:
  -h, --help            show this help message and exit

Subcommand: ``begin``
---------------------

usage::

       nerd-dictation begin [-h] [--cookie FILE_PATH] [--config FILE]
                            [--vosk-model-dir DIR] [--vosk-grammar-file DIR]
                            [--pulse-device-name IDENTIFIER]
                            [--sample-rate HZ] [--defer-output] [--continuous]
                            [--timeout SECONDS] [--idle-time SECONDS]
                            [--delay-exit SECONDS] [--suspend-on-start]
                            [--punctuate-from-previous-timeout SECONDS]
                            [--full-sentence] [--numbers-as-digits]
                            [--numbers-use-separator]
                            [--numbers-min-value NUMBERS_MIN_VALUE]
                            [--numbers-no-suffix] [--input INPUT_METHOD]
                            [--output OUTPUT_METHOD]
                            [--simulate-input-tool SIMULATE_INPUT_TOOL]
                            [--verbose VERBOSE] [- ...]

This creates the directory used to store internal data, so other commands such as sync can be performed.

options:
  -h, --help            show this help message and exit
  --cookie FILE_PATH    Location for writing a temporary cookie (this file is monitored to begin/end dictation).
  --config FILE         Override the file used for the user configuration.
                        Use an empty string to prevent the users configuration being read.
  --vosk-model-dir DIR  Path to the VOSK model, see: https://alphacephei.com/vosk/models
  --vosk-grammar-file DIR
                        Path to a JSON grammar file.  This restricts the phrases recognized by VOSK for
                        better accuracy.  See `vosk_recognizer_new_grm` in the API reference:
                        https://github.com/alphacep/vosk-api/blob/master/src/vosk_api.h
  --pulse-device-name IDENTIFIER
                        The name of the pulse-audio device to use for recording.
                        See the output of "pactl list sources" to find device names (using the identifier following "Name:").
  --sample-rate HZ      The sample rate to use for recording (in Hz).
                        Defaults to 44100.
  --defer-output        When enabled, output is deferred until exiting.

                        This prevents text being typed during speech (implied with ``--output=STDOUT``)
  --continuous          Enable this option, when you intend to keep the dictation process enabled for extended periods of time.
                        without this enabled, the entirety of this dictation session will be processed on every update.
                        Only used when ``--defer-output`` is disabled.
  --timeout SECONDS     Time out recording when no speech is processed for the time in seconds.
                        This can be used to avoid having to explicitly exit (zero disables).
  --idle-time SECONDS   Time to idle between processing audio from the recording.
                        Setting to zero is the most responsive at the cost of high CPU usage.
                        The default value is 0.1 (processing 10 times a second), which is quite responsive in practice
                        (the maximum value is clamped to 0.5)
  --delay-exit SECONDS  The time to continue running after an end request.
                        this can be useful so "push to talk" setups can be released while you finish speaking
                        (zero disables).
  --suspend-on-start    Start the process and immediately suspend.
                        Intended for use when nerd-dictation is kept open
                        where resume/suspend is used for dictation instead of begin/end.
  --punctuate-from-previous-timeout SECONDS
                        The time-out in seconds for detecting the state of dictation from the previous recording,
                        this can be useful so punctuation it is added before entering the dictation(zero disables).
  --full-sentence       Capitalize the first character.
                        This is also used to add either a comma or a full stop when dictation is performed under the
                        ``--punctuate-from-previous-timeout`` value.
  --numbers-as-digits   Convert numbers into digits instead of using whole words.
  --numbers-use-separator
                        Use a comma separators for numbers.
  --numbers-min-value NUMBERS_MIN_VALUE
                        Minimum value for numbers to convert from whole words to digits.
                        This provides for more formal writing and prevents terms like "no one"
                        from being turned into "no 1".
  --numbers-no-suffix   Suppress number suffixes when --numbers-as-digits is specified.
                        For example, this will prevent "first" from becoming "1st".
  --input INPUT_METHOD  Specify input method to be used for audio recording. Valid methods: PAREC, SOX

                        - ``PAREC`` (external command, default)
                          See --pulse-device-name option to use a specific pulse-audio device.
                        - ``SOX`` (external command)
                          For help on setting up sox, see ``readme-sox.rst`` in the nerd-dictation repository.
  --output OUTPUT_METHOD
                        Method used to at put the result of speech to text.

                        - ``SIMULATE_INPUT`` simulate keystrokes (default).
                        - ``STDOUT`` print the result to the standard output.
                          Be sure only to handle text from the standard output
                          as the standard error may be used for reporting any problems that occur.
  --simulate-input-tool SIMULATE_INPUT_TOOL
                        Program used to simulate keystrokes (default).

                        - ``XDOTOOL`` Compatible with the X server only (default).
                        - ``DOTOOL`` Compatible with all Linux distributions and Wayland.
                        - ``DOTOOLC`` Same as DOTOOL but for use with the `dotoold` daemon.
                        - ``YDOTOOL`` Compatible with all Linux distributions and Wayland but requires some setup.
                        - ``WTYPE`` Compatible with Wayland.
                          For help on setting up ydotool, see ``readme-ydotool.rst`` in the nerd-dictation repository.
  --verbose VERBOSE     Verbosity level, defaults to zero (no output except for errors)

                        - Level 1: report top level actions (dictation started, suspended .. etc).
                        - Level 2: report internal details (may be noisy).
  ``-`` ...             End argument parsing.
                        This can be used for user defined arguments which configuration scripts may read from the ``sys.argv``.

Subcommand: ``end``
-------------------

usage::

       nerd-dictation end [-h] [--cookie FILE_PATH]

This ends dictation, causing the text to be typed in.


options:
  -h, --help          show this help message and exit
  --cookie FILE_PATH  Location for writing a temporary cookie (this file is monitored to begin/end dictation).

Subcommand: ``cancel``
----------------------

usage::

       nerd-dictation cancel [-h] [--cookie FILE_PATH]

This cancels dictation.

options:
  -h, --help          show this help message and exit
  --cookie FILE_PATH  Location for writing a temporary cookie (this file is monitored to begin/end dictation).

Subcommand: ``suspend``
-----------------------

usage::

       nerd-dictation suspend [-h] [--cookie FILE_PATH]

Suspend recording audio & the dictation process.

This is useful on slower systems or when large language models take longer to load.
Recording audio is stopped and the process is paused to remove any CPU overhead.

options:
  -h, --help          show this help message and exit
  --cookie FILE_PATH  Location for writing a temporary cookie (this file is monitored to begin/end dictation).

Subcommand: ``resume``
----------------------

usage::

       nerd-dictation resume [-h] [--cookie FILE_PATH]

Resume recording audio & the dictation process.

This is to be used to resume after the 'suspend' command.
When nerd-dictation is not suspended, this does nothing.

options:
  -h, --help          show this help message and exit
  --cookie FILE_PATH  Location for writing a temporary cookie (this file is monitored to begin/end dictation).

.. END HELP TEXT


Details
=======

- Typing in results will **never** press enter/return.
- Recording and speech to text is performed in parallel.


Examples
========


Store the result of speech to text as a variable in the shell:

.. code-block:: sh

   SPEECH="$(nerd-dictation begin --timeout=1.0 --output=STDOUT)"


Example Configurations
----------------------

These are example configurations you may use as a reference.

- `Word Replacement
  <https://github.com/ideasman42/nerd-dictation/blob/master/examples/default/nerd-dictation.py>`__.
- `Start/Finish Commands
  <https://github.com/ideasman42/nerd-dictation/blob/master/examples/begin_end_commands/nerd-dictation.py>`__.


Other Software
==============

- `Elograf <https://github.com/papoteur-mga/elograf>`__ - nerd-dictation GUI front-end that runs as a tray icon.
- `Numen <https://numen.johngebbie.com>`__ - voice input for desktop computing that also uses VOSK.


Limitations
===========

- Text from VOSK is all lower-case,
  while the user configuration can be used to set the case of common words like ``I`` this isn't very convenient
  (see the example configuration for details).

- For some users the delay in start up may be noticeable on systems with slower hard disks
  especially when running for the 1st time (a cold start).

  This is a limitation with the choice not to use a service that runs in the background.
  Recording begins before any the speech-to-text components are loaded to mitigate this problem.


Further Work
============

- Support a general solution to capitalize words (proper nouns for example).
- Possibly other speech to text engines *(only if they provide some significant benefits)*.
- Possibly support Windows & macOS.
