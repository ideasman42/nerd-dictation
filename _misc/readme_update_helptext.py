#!/usr/bin/env python3
# GPL License, Version 3.0 or later

import os
import subprocess
import re

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
COMMAND_NAME = "nerd-dictation"


def patch_help_test_all(help_output):
    help_output = help_output.replace(
        "usage: " + COMMAND_NAME,
        "usage::\n"
        "\n"
        "       " + COMMAND_NAME,
    )
    return help_output


def patch_help_test_main(help_output):
    help_output = help_output.replace('{begin,end,cancel}', '')
    help_output = re.sub(r"[ \t]+(\n|\Z)", r"\1", help_output)

    help_output = help_output.replace("    begin ", "    :begin: ")
    help_output = help_output.replace("    end ", "    :end: ")
    help_output = help_output.replace("    cancel ", "    :cancel: ")
    return help_output


def patch_help_test_for_begin(help_output):
    # Needed so the '-' argument is not interpreted as a dot-point.
    help_output = help_output.replace(
        " - ...     ",
        " ``-`` ... ",
    )
    return help_output


def main():
    base_command = "python3", os.path.join(BASE_DIR, COMMAND_NAME)
    p = subprocess.run(
        [*base_command, "--help"],
        stdout=subprocess.PIPE,
    )
    help_output = [(p.stdout.decode("utf-8").rstrip() + "\n\n")]

    for sub_command in ("begin", "end", "cancel"):
        p = subprocess.run([*base_command, sub_command, "--help"], stdout=subprocess.PIPE)
        title = "Subcommand: ``" + sub_command + "``"
        help_output.append(
            title + "\n" +
            ("-" * len(title)) + "\n\n" +
            p.stdout.decode("utf-8").rstrip() +
            "\n\n"
        )

    # strip trailing space
    for i in range(len(help_output)):
        help_output[i] = re.sub(r"[ \t]+(\n|\Z)", r"\1", help_output[i])
        help_output[i] = patch_help_test_all(help_output[i])

    help_output[0] = patch_help_test_main(help_output[0])
    help_output[1] = patch_help_test_for_begin(help_output[1])

    help_output[0] = (
        "\nOutput of ``" + COMMAND_NAME + " --help``\n\n" +
        help_output[0]
    )

    with open("readme.rst", "r", encoding="utf-8") as f:
        data = f.read()

    help_begin_text = ".. BEGIN HELP TEXT"
    help_end_text = ".. END HELP TEXT"
    help_begin_index = data.find(help_begin_text)
    help_end_index = data.find(help_end_text, help_begin_index)

    if help_begin_index == -1:
        print("Error: {!r} not found".format(help_begin_text))
        return
    if help_end_index == -1:
        print("Error: {!r} not found".format(help_end_text))
        return

    help_begin_index += len(help_begin_text) + 1

    data_update = data[:help_begin_index] + "".join(help_output) + data[help_end_index:]

    with open("readme.rst", "w", encoding="utf-8") as f:
        f.write(data_update)


if __name__ == "__main__":
    main()
