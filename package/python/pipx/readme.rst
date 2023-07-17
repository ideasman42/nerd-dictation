##################
Packaging with pipx
##################

To install ``nerd-dictaiton`` in an isolated environment with ``pipx``, run:

.. code-block:: sh

   git clone https://github.com/ideasman42/nerd-dictation.git
   cd nerd-dictation
   mv ./package/python/pipx/pyproject.toml ./
   pipx install .

On a typical Linux system, this will install ``nerd-dictation`` to ``~/.local/bin``.
