##############
Nerd Dictation
##############

*Offline Speech to Text for Desktop Linux.*

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

The key features for this tool are.



Specific features include:

``--numbers-as-digits``

   Optional conversion from numbers to digits.

   So ``Three million five hundred and sixty second`` becomes ``3,000,562nd``.

   A series of numbers (such as reciting a phone number) is also supported.

   So ``Two four six eight`` becomes ``2,468``.


Dependencies
============

- Python 3.
- The VOSK-API.
- ``parec`` command (for recording from pulse-audio).
- ``xdotool`` command to simulate keyboard input.


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


Details
=======

- Typing in results will **never** press enter/return.
- Pulse audio is used for recording.
- Recording and speech to text a performed in parallel.


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

- And a general solution to capitalize words (proper nouns for example).
- Preview output while dictating.
- Wayland support (this should be quite simple to support and mainly relies on a replacement for ``xdotool``).
- Add a ``setup.py`` for easy installation on uses systems.
- Possibly other speech to text engines *(only if they provide some significant benefits)*.
- Possibly support Windows & macOS.
