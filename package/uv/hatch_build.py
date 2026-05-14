# Custom hatchling build hook that eliminates file duplication.
#
# The entire application lives in a single script at the repo root
# (../../nerd-dictation).  Rather than track a copy inside this package
# directory, this hook injects it into the wheel via build_data["force_include"],
# mapping the script to nerd_dictation/__init__.py.
#
# Two source locations are handled:
#   - Source tree:  ../../nerd-dictation  (relative to package/uv)
#   - Sdist tree:    ./nerd-dictation       (force-include places it at root)

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import os


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "sync_source"

    def initialize(self, version, build_data):
        # When building from the source tree, the script is two dirs up.
        src = os.path.normpath(os.path.join(self.root, "..", "..", "nerd-dictation"))

        # When building from an sdist, force-include already placed it at root.
        if not os.path.exists(src):
            alt = os.path.join(self.root, "nerd-dictation")
            if os.path.exists(alt):
                src = alt

        if os.path.exists(src):
            build_data["force_include"][src] = "nerd_dictation/__init__.py"
