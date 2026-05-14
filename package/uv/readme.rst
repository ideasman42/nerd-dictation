###################
Packaging with uv
###################

To install ``nerd-dictation`` as a tool using `uv <https://docs.astral.sh/uv/>`_:

From a local clone:

.. code-block:: sh

   git clone https://github.com/ideasman42/nerd-dictation.git
   cd nerd-dictation
   uv tool install ./package/uv

Or directly from the remote repository:

.. code-block:: sh

   uv tool install "git+https://github.com/ideasman42/nerd-dictation.git#subdirectory=package/uv"

After installing, download a VOSK model:

.. code-block:: sh

   nerd-dictation download-model

See the main `readme.rst <../../readme.rst>`_ for full usage instructions.