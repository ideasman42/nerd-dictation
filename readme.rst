##############
Nerd Dictation
##############

*Offline Speech to Text for Desktop Linux.* - See `demo video <https://www.youtube.com/watch?v=T7sR-4DFhpQ>`__.

This is a utility that provides simple access speech to text for using in Linux
without being tied to a desktop environment.

Simple
   This is a single file Python script with minimal dependencies.
Hackable
   User configuration lets you manipulate text using Python string operations.
Zero Overhead
   As this relies on manual activation there are no background processes.

Dictation is accessed manually with begin/end commands.

This uses the excellent `vosk-api <https://github.com/alphacep/vosk-api>`__.


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

See ``nerd-dictation begin --help`` for details on how to access these options.


Dependencies
============

- Python 3.
- The VOSK-API.
- ``parec`` command for recording from pulse-audio (default) or ``sox`` command as alternative.
- ``xdotool`` (default, X11 only) or
  ``ydotool`` command to simulate keyboard input (supports X11 & Wayland).
  See the ``ydotool`` setup guide: `Using ydotool with nerd-dictation <readme-ydotool.rst>`_.


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

This is a utility that activates text to speech in Linux.
While it could use any system currently it uses the VOSK-API.

positional arguments:

    :begin:             Begin dictation.
    :end:               End dictation.
    :cancel:            Cancel dictation.

options:
  -h, --help          show this help message and exit

Subcommand: ``begin``
---------------------

usage::

       nerd-dictation begin [-h] [--cookie FILE_PATH] [--config FILE]
                            [--vosk-model-dir DIR]
                            [--pulse-device-name IDENTIFIER]
                            [--sample-rate HZ] [--defer-output] [--continuous]
                            [--timeout SECONDS] [--idle-time SECONDS]
                            [--delay-exit SECONDS]
                            [--punctuate-from-previous-timeout SECONDS]
                            [--full-sentence] [--numbers-as-digits]
                            [--numbers-use-separator] [--input INPUT_METHOD]
                            [--output OUTPUT_METHOD]
                            [--simulate-input-tool SIMULATE_INPUT_TOOL]
                            [- ...]

This creates the directory used to store internal data, so other commands such as sync can be performed.


options:
  -h, --help            show this help message and exit
  --cookie FILE_PATH    Location for writing a temporary cookie (this file is monitored to begin/end dictation).
  --config FILE         Override the file used for the user configuration.
                        Use an empty string to prevent the users configuration being read.
  --vosk-model-dir DIR  Path to the VOSK model, see: https://alphacephei.com/vosk/models
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
  --delay-exit SECONDS  The time to continue running after an exit request.
                        this can be useful so "push to talk" setups can be released while you finish speaking
                        (zero disables).
  --punctuate-from-previous-timeout SECONDS
                        The time-out in seconds for detecting the state of dictation from the previous recording, this can be useful so punctuation it is added before entering the dictation(zero disables).
  --full-sentence       Capitalize the first character.
                        This is also used to add either a comma or a full stop when dictation is performed under the
                        ``--punctuate-from-previous-timeout`` value.
  --numbers-as-digits   Convert numbers into digits instead of using whole words.
  --numbers-use-separator
                        Use a comma separators for numbers.
  --input INPUT_METHOD  Specify input method to be used for audio recording. Valid methods: PAREC, SOX

                        - ``PAREC`` (external command, default)
                          See --pulse-device-name option to use a specific pulse-audio device.
                        - ``SOX`` (external command)
                          Set environment variable AUDIODEV to use a specific input device.
                          Other sox options can be set (such as gain) by setting environment variable SOX_OPTS.
                          You can test various devices by::

                             # List audio devices.
                             arecord -l || cat /proc/asound/cards || cat /dev/sndstat

                             # Example, use card 2, subdevice 0.
                             # Record 10 seconds and playback to default output.
                             AUDIODEV='hw:2,0' \
                                 sox -d --buffer 1000 -r 16000 -b 16 -e signed-integer \
                                 -c 1 -t wav -L test.wav trim 0 10
                             sox test.wav -d
  --output OUTPUT_METHOD
                        Method used to at put the result of speech to text.

                        - ``SIMULATE_INPUT`` simulate keystrokes (default).
                        - ``STDOUT`` print the result to the standard output.
                          Be sure only to handle text from the standard output
                          as the standard error may be used for reporting any problems that occur.
  --simulate-input-tool SIMULATE_INPUT_TOOL
                        Program used to simulate keystrokes (default).

                        - ``XDOTOOL`` Compatible with the X server only (default).
                        - ``YDOTOOL`` Compatible with all Linux distributions and Wayland but requires some setup.
                          For help on setting up ydotool, see our guide readme-ydotool.rst in the nerd-dictation repository.
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

.. END HELP TEXT


Details
=======

- Typing in results will **never** press enter/return.
- Pulse audio is used for recording.
- Recording and speech to text a performed in parallel.


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
- Add a ``setup.py`` for easy installation on uses systems.
- Possibly other speech to text engines *(only if they provide some significant benefits)*.
- Possibly support Windows & macOS.
