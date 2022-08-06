##############
Nerd Dictation
##############

*Offline Speech to Text for Desktop Linux.* - See `demo video <https://www.youtube.com/watch?v=T7sR-4DFhpQ>`__.

This is a utility that provides simple access speech to text for using in Linux
without being tied to a desktop environment, using the excellent `VOSK-API <https://github.com/alphacep/vosk-api>`__.

This is a simple `nix-shell <https://nixpkgs.org>` wrapper and ``default.nix`` that bundles all of the dependencies and one of two English language models into a turn-key environment.

You can use the ``default.nix`` in your own Nix derivations, though you will need to include the ``vosk`` dependency as it is not in mainline nixpkgs at time of writing.

Usage
=====

From the root of the cloned project:

.. code-block:: sh

    $ cd package/nix
    $ nix-shell

Once that is finished successfully you will be in a shell that lets you run the ``nerd-dictation`` commands as normal.

.. hint::

    The shell will download the small English language model by default and export its path in the ``VOSK_MODEL_EN`` environment variable. Allowing you to use the following command:

.. code-block:: sh

    $ nerd-dictation begin --vosk-model-dir=$VOSK_MODEL_EN &

Other models may be used as you wish and referenced in the usual manner.
