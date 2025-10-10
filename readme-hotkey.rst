Hotkey Activation for Nerd Dictation
====================================

This document describes the hotkey functionality for nerd-dictation, which provides
instant voice-to-text activation using a double-tap hotkey.

Features
--------

- **Double-tap activation**: Quick double-tap to toggle dictation on/off
- **Configurable hotkeys**: Choose from Caps Lock (default), Right Alt, AltGr, or Menu key
- **Audio feedback**: Plays sounds when starting/stopping dictation
- **Model ready detection**: Prevents activation attempts before model loads (with error sound)
- **Fast response**: Keeps model loaded in memory using suspend/resume
- **Auto-recovery**: Automatically restarts if nerd-dictation crashes
- **Device selection**: Support for specific audio input devices
- **Instance management**: Prevents duplicate processes and cleans up orphaned instances

Installation
------------

1. Install the required Python module:

   .. code-block:: bash

      pip install pynput

2. Ensure you have audio playback support (PipeWire or PulseAudio)

3. Place the ``hotkey.py`` script in your nerd-dictation directory

Usage
-----

Basic usage with default settings (double-tap Caps Lock):

.. code-block:: bash

   python hotkey.py

Use a different activation key:

.. code-block:: bash

   # Right Alt key
   python hotkey.py --key alt_r

   # AltGr key (international keyboards)
   python hotkey.py --key alt_gr

   # Menu/Compose key
   python hotkey.py --key menu

Specify an audio device:

.. code-block:: bash

   python hotkey.py --device "alsa_input.usb-webcam.analog-stereo"

Configuration
-------------

The script uses the following settings:

- **Double-tap timeout**: 300ms between taps
- **Audio format**: 16kHz sample rate (optimal for speech recognition)
- **Input method**: PW-CAT (PipeWire) or SOX
- **Output method**: SIMULATE_INPUT with xdotool

Sound Files
-----------

The script uses audio feedback to indicate different states:

- ``sounds/ready.wav``: Played once when the model finishes loading (startup complete)
- ``sounds/start.wav``: Played when dictation is activated (microphone on)
- ``sounds/stop.wav``: Played when dictation is suspended (microphone off)
- ``sounds/error.wav``: Played when errors occur:
  
  - Model not ready yet (double-tap before startup completes)
  - Process crashes or fails to start
  - Out of memory errors

If these files don't exist, the script will run silently.

**Startup sequence**: When you first run the script, you'll see "Waiting for model to load..." 
and after a few seconds (depending on model size), you'll hear the ready sound indicating 
the system is ready for dictation.

The included sounds are derived from Pixabay and are free for use under the Pixabay Content
License. See ``sounds/LICENSE.md`` for attribution details.

Troubleshooting
---------------

**No text appears when speaking:**

- Check that your microphone is working and not muted
- Verify the VOSK model is properly installed in ``~/.config/nerd-dictation/model``
- Try running ``nerd-dictation begin --verbose 2`` directly to debug

**Double-tap not detected:**

- Ensure you're tapping quickly enough (within 300ms)
- Some keyboards may have limitations with certain keys
- Try using a different activation key

**"xdotool not found" error:**

- Install xdotool: ``sudo apt install xdotool`` (Debian/Ubuntu)
- For Wayland, you may need to configure ``--simulate-input-tool`` differently

Technical Details
-----------------

The hotkey script:

1. **Startup safety**: Checks for and cleans up any existing nerd-dictation processes
2. **Process management**: Prevents multiple instances of hotkey.py from running
3. **Model loading**: Starts nerd-dictation in suspended state and monitors output
4. **Ready detection**: Plays a sound when model is loaded and ready for use
5. **Keyboard monitoring**: Uses double-tap detection to avoid accidental activation
6. **Fast toggling**: Sends resume/suspend commands for instant response
7. **Error handling**: Plays error sounds and provides clear messages on failures
8. **Memory protection**: Monitors for out-of-memory conditions
9. **Clean shutdown**: Properly stops processes and removes PID files on exit

This approach provides near-instant activation compared to loading the model
each time dictation starts, while preventing system resource issues.

Desktop Autostart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``~/.config/autostart/nerd-dictation-hotkey.desktop``:

.. code-block:: ini

   [Desktop Entry]
   Type=Application
   Name=Nerd Dictation Hotkey
   Comment=Double-tap Caps Lock for voice dictation
   Exec=/path/to/nerd-dictation/hotkey.py
   Icon=audio-input-microphone
   Hidden=false
   NoDisplay=false
   X-GNOME-Autostart-enabled=true
   StartupNotify=false
   Terminal=false

Or use your desktop environment's GUI:

- **GNOME**: Settings → Startup Applications
- **KDE**: System Settings → Startup and Shutdown → Autostart
- **XFCE**: Settings Manager → Session and Startup → Application Autostart
