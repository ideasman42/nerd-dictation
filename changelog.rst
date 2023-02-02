
#########
Changelog
#########

- 2023/02/02: Add ``suspend`` & ``resume`` sub-commands for process level suspend/resume.
- 2022/11/03: Add ``dotool`` support with ``--simpulate-input-tool=DOTOOL``.
- 2022/06/05: Add packaging script for PIP/setup-tools to optionally install via PIP.
- 2022/05/16: Add ``ydotool`` support with ``--simpulate-input-tool=YDOTOOL``.
- 2022/04/18: Add ``--input`` option to specify audio recording command, added ``sox`` input.
- 2022/01/21: Add ``--config`` option to specify a custom configuration file location.
- 2022/01/21: Correct error reporting an error when evaluating the user configuration fails.
- 2022/01/10: Improve error message when ``xdotool`` is not found.
- 2022/01/09: Fix ``--numbers-as-digits`` bug where numbers with the same decimal place value where accumulated,
  e.g. "one hundred two hundred" is now interrupted as "100 200" instead of "10,200".
- 2022/01/05: Fix ``--numbers-as-digits`` bug adding where quoted numbers would accumulate,
  e.g. "one hundred and fifty twelve" would be interpreted as "162" instead of "150 12".
- 2022/01/05: Fix bug interpreting a series of numbers over 9, as well as stripping leading zeros.
- 2021/10/05: Fix bug where quickly running begin/end would leave dictation enabled.
- 2021/07/08: Add ``--sample-rate``, optionally set the sample rate used for recording.
- 2021/06/25: Add ``--idle-time``, optionally idle to avoid high CPU usage for no perceptual gain (fixes #6).
- 2021/06/07: Add ``--delay-exit``, convenient when pushed to talk is used.
- 2021/06/07: Improve recording logic to capture more of the end of the recording before exiting.
- 2021/05/30: Fix error with ``xdotool`` mistaking text as arguments.
- 2021/05/30: Fix adding numbers with "and", "one and two" now resolve to "1 and 2" not "3".
- 2021/05/30: Add numeric scales up to 'centillion' (10**303).
- 2021/05/30: Fix error converting isolated scales to numerals so ``thousands`` becomes ``1000s``.
- 2021/05/29: Support typing during dictation (disable with ``--defer-output``).
- 2021/05/28: Add ``--timeout`` flag to finish when no speech is detected for a given number of seconds.
- 2021/05/27: Add an ``--output`` flag so text can be printed to the standard output using ``--output=STDOUT``.
  which may be useful for some tasks.
- 2021/05/27: Ignore arguments after ``-`` (so they can be read by user configuration script).
