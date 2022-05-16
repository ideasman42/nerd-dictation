#####################################
Using ``ydotool`` with nerd-dictation
#####################################

This guide explains how to get and configure ``ydotool`` to simulate typing with ``nerd-dictation``,
which brings support for typing on Wayland and languages other than English.

When should I use ``ydotool``?
==============================

By default, ``nerd-dictation`` uses the ``xdotool`` program to simulate writing with the keyboard.

This program has two major limitations:

#. It is only compatible with Xorg, not with Wayland.
   If you want to use Wayland, the program will not type anything.
#. It suffers from considerable slowdowns when writing characters not found in the English language,
   temporarily freezing your computer's display.

There is a program named ``ydotool`` that you can use as an alternative to ``xdotool``.
``ydotool`` does not rely on the X server, so it is compatible with Wayland.

It also offers better performance in languages other than English.

The flip side is that it requires some system configuration to use conveniently.
Also, it lacks accessible documentation, which is why it is not the default.

Installing ``ydotool``
======================

You will need to download the latest version of the program found on its git repository:
https://github.com/ReimuNotMoe/ydotool/releases/

There, you can download compiled executables.
You should then place them in a place that's available on your ``$PATH`` environment variable.

**Warning:** While ``ydotool`` is available on the ``apt`` package manager on Ubuntu 22.04 LTS,
the Debian package is outdated.

Configuring ``ydotool``
=======================

To simulate typing, the program needs access to your ``/dev/uinput`` device.
By default, this requires root privileges every time you run ``ydotool``,
so you'd have to enter your password every time you run ``nerd-dictation``.

To avoid that, you can give the program permanent access to the input device by adding your username to the ``input``
user group on your system and giving the group write access to the ``uinput`` device.

To do that, we use a udev rule.
Udev is the Linux system that detects and reacts to devices getting plugged or unplugged on your computer.
It also works with virtual devices like ``ydotool``.

To add a user to a group, you can use the ``usermod`` command, like so:

.. code-block:: sh

   # Append YOUR_USERNAME to the group named "input"
   sudo usermod -aG input YOUR_USERNAME

To get your username, you can use the variable $USER or $USERNAME.

.. code-block:: sh

   sudo usermod -aG input $USERNAME

You then need to define a new udev rule that will give the ``input`` group permanent write access to the uinput device
(this will give ``ydotool`` write access too).

.. code-block:: sh

    echo '## Give ydotoold access to the uinput device
    ## Solution by https://github.com/ReimuNotMoe/ydotool/issues/25#issuecomment-535842993
    KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"
    ' | sudo tee /etc/udev/rules.d/80-uinput.rules > /dev/null

You will need to restart your computer for the change to take effect.

Finally, ``ydotool`` works with a daemon that you leave running in the background, ``ydotoold``,
for performance reasons. You needs to run ``ydotoold`` before you start using ``ydotool``.

To avoid running it every time you start the computer, you can add it to your startup programs.
The steps depend on your distribution, so we'll let you look this up.

Running nerd dictation with ``ydotool``
=======================================

To run ``nerd-dictation`` with ``ydotool``, use the ``--simulate-input-tool`` argument.

.. code-block:: sh

   nerd-dictation begin --simulate-input-tool=YDOTOOL
