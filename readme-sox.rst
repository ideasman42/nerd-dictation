#################################
Using ``sox`` with nerd-dictation
#################################

This guide explains how to configure ``sox`` for recording audio with ``nerd-dictation``.


When should I use ``sox``?
==========================

You may wish to configure ``sox`` if you are using a system without pulse-audio support (such as FreeBSD).


Configuring ``sox``
===================

Set environment variable ``AUDIODEV`` to use a specific input device.
Other sox options can be set (such as gain) by setting environment variable ``SOX_OPTS``.

You can test various devices by

.. code-block:: sh

   # List audio devices.
   arecord -l || cat /proc/asound/cards || cat /dev/sndstat

   # Example, use card 2, subdevice 0.
   # Record 10 seconds and playback to default output.
   AUDIODEV='hw:2,0' sox -d --buffer 1000 -r 16000 -b 16 -e signed-integer -c 1 -t wav -L test.wav trim 0 10
   sox test.wav -d


Running nerd dictation with ``sox``
===================================

To run ``nerd-dictation`` with ``sox``, use the ``--input`` argument.

.. code-block:: sh

   nerd-dictation begin --input=SOX
