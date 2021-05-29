
#########
Changelog
#########

- 2021/05/30: Add numeric scales up to 'centillion' (10**303).
- 2021/05/30: Fix error converting isolated scales to numerals so ``thousands`` becomes ``1000s``.
- 2021/05/29: Support typing during dictation (disable with ``--defer-output``).
- 2021/05/28: Add ``--timeout`` flag to finish when no speech is detected for a given number of seconds.
- 2021/05/27: Add an ``--output`` flag so text can be printed to the standard output using ``--output=STDOUT``.
  which may be useful for some tasks.
- 2021/05/27: Ignore arguments after ``-`` (so they can be read by user configuration script).