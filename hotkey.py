#!/usr/bin/env python3
"""
Hotkey activation for nerd-dictation.

This script provides hotkey activation for nerd-dictation using double-tap
detection. It keeps the speech recognition model loaded in memory and uses
suspend/resume for instant response times.

Features:
- Double-tap activation (default: Caps Lock, configurable)
- Audio feedback with start/stop sounds
- Automatic process recovery if nerd-dictation crashes
- Support for custom audio devices

Usage:
    python hotkey.py [--device DEVICE] [--key KEY]

Examples:
    python hotkey.py                   # Use defaults
    python hotkey.py --key alt_r       # Use right Alt key
    python hotkey.py --device "webcam" # Use specific audio device
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional

try:
    from pynput import keyboard
except ImportError:
    print("Error: pynput module not found. Install with: pip install pynput")
    sys.exit(1)


class PushToTalkController:
    def __init__(self, device_name: Optional[str] = None, activation_key: str = "caps_lock"):
        self.device_name = device_name
        self.activation_key = activation_key.lower()  # Key to double-tap
        self.script_dir = Path(__file__).parent.absolute()

        # Check for existing instances
        self._check_existing_instances()

        # Try to find nerd-dictation executable
        self.nerd_dictation = self._find_nerd_dictation()

        # Use current Python interpreter (works with venv, system python, etc.)
        self.python_exe = sys.executable

        # PID file for tracking
        self.pid_file = Path.home() / ".local" / "share" / "nerd-dictation-hotkey.pid"

        # Sound files
        self.ready_sound = self.script_dir / "sounds" / "ready.wav"
        self.start_sound = self.script_dir / "sounds" / "start.wav"
        self.stop_sound = self.script_dir / "sounds" / "stop.wav"
        self.error_sound = self.script_dir / "sounds" / "error.wav"  # Not ready/error sound

        self.dictation_process: Optional[subprocess.Popen] = None
        self.is_suspended = True
        self.is_active = False  # Track if dictation is active
        self.is_ready = False  # Track if model is loaded
        self.last_tap_time = {}  # Track last tap time for each key
        self.double_tap_timeout = 0.3  # 300ms for double tap

    def _check_existing_instances(self):
        """Check for and clean up existing instances."""
        # Clean up any orphaned nerd-dictation processes
        try:
            # Find existing nerd-dictation processes
            result = subprocess.run(["pgrep", "-f", "nerd-dictation begin"], capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split("\n")
                print(f"Found {len(pids)} existing nerd-dictation process(es), cleaning up...")
                for pid in pids:
                    try:
                        subprocess.run(["kill", "-9", pid], check=False)
                    except:
                        pass
                time.sleep(1)
        except:
            pass

        # Check for existing hotkey.py instances
        try:
            result = subprocess.run(["pgrep", "-f", "python.*hotkey.py"], capture_output=True, text=True)
            if result.stdout.strip():
                pids = [p for p in result.stdout.strip().split("\n") if p != str(os.getpid())]
                if pids:
                    print(f"ERROR: hotkey.py is already running (PID: {pids[0]})")
                    print("Please stop the existing instance first")
                    sys.exit(1)
        except:
            pass

    def _find_nerd_dictation(self) -> Path:
        """Find nerd-dictation executable in various locations."""
        # Check common locations
        locations = [
            self.script_dir / "nerd-dictation",
            Path("nerd-dictation"),  # In PATH
            Path("/usr/local/bin/nerd-dictation"),
            Path("/usr/bin/nerd-dictation"),
        ]

        for loc in locations:
            if loc.exists() or subprocess.run(["which", str(loc)], capture_output=True).returncode == 0:
                return loc

        print("Error: Could not find nerd-dictation executable")
        print("Please ensure nerd-dictation is in your PATH or in the same directory as this script")
        sys.exit(1)

    def toggle_dictation(self):
        """Toggle dictation on/off."""
        # Check if ready first
        if not self.is_ready:
            print("Model not ready yet, please wait...")
            self.play_sound(self.error_sound)
            return

        if self.is_active:
            self.is_active = False
            self.suspend_dictation()
        else:
            self.is_active = True
            self.resume_dictation()

    def play_sound(self, sound_file: Path):
        """Play a sound file using pw-play or paplay."""
        if not sound_file.exists():
            return

        try:
            # Try pw-play first (PipeWire)
            subprocess.run(
                ["pw-play", str(sound_file)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Fall back to paplay (PulseAudio)
                subprocess.run(
                    ["paplay", str(sound_file)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                # If neither works, silently continue
                pass

    def start_nerd_dictation(self):
        """Start nerd-dictation process in suspended state."""
        print("Starting nerd-dictation (loading model, this may take a moment)...")

        cmd = [
            str(self.python_exe),
            str(self.nerd_dictation),
            "begin",
            "--input",
            "PW-CAT",
            "--output",
            "SIMULATE_INPUT",
            "--simulate-input-tool",
            "XDOTOOL",
            "--sample-rate",
            "16000",  # Use 16kHz which is standard for speech recognition
            "--timeout",
            "0",  # Disable timeout
            "--continuous",  # Enable continuous mode for better performance
            "--suspend-on-start",  # Start suspended
            "--verbose",
            "1",  # Basic verbosity
        ]

        # Only add device name if specified
        if self.device_name:
            cmd.extend(["--pulse-device-name", self.device_name])

        try:
            # Capture output to monitor for "Model loaded" message
            self.dictation_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
            )
            print(f"Started nerd-dictation process (PID: {self.dictation_process.pid})")
            print("Waiting for model to load...")

            # Start thread to monitor output
            def monitor_output():
                for line in self.dictation_process.stdout:
                    print(line.strip())
                    if "Model loaded" in line:
                        self.is_ready = True
                        print("Model is ready!")
                        # Play a ready sound
                        self.play_sound(self.ready_sound)
                        break
                    # Check for memory warnings
                    if "MemoryError" in line or "out of memory" in line.lower():
                        print("ERROR: Out of memory! Stopping...")
                        self.play_sound(self.error_sound)
                        self.stop_nerd_dictation()
                        sys.exit(1)

            monitor_thread = threading.Thread(target=monitor_output, daemon=True)
            monitor_thread.start()

            # Wait a bit to see if it crashes immediately
            time.sleep(1)
            if self.dictation_process.poll() is not None:
                print(f"ERROR: nerd-dictation process died with exit code: {self.dictation_process.returncode}")
                self.play_sound(self.error_sound)
                sys.exit(1)
        except Exception as e:
            print(f"Error starting nerd-dictation: {e}")
            self.play_sound(self.error_sound)
            sys.exit(1)

    def resume_dictation(self):
        """Resume dictation."""
        if not self.is_suspended:
            return

        # Check if process is still alive
        if self.dictation_process and self.dictation_process.poll() is not None:
            print(f"ERROR: nerd-dictation process died! Exit code: {self.dictation_process.returncode}")
            print("Restarting nerd-dictation...")
            self.start_nerd_dictation()

        print("Resuming dictation...")
        self.play_sound(self.start_sound)

        cmd = [str(self.python_exe), str(self.nerd_dictation), "resume"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if result.stderr:
                print(f"Resume stderr: {result.stderr}")
            self.is_suspended = False
        except subprocess.CalledProcessError as e:
            print(f"Error resuming dictation: {e}")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")

    def suspend_dictation(self):
        """Suspend dictation."""
        if self.is_suspended:
            return

        print("Suspending dictation...")
        self.play_sound(self.stop_sound)

        cmd = [str(self.python_exe), str(self.nerd_dictation), "suspend"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if result.stderr:
                print(f"Suspend stderr: {result.stderr}")
            self.is_suspended = True
        except subprocess.CalledProcessError as e:
            print(f"Error suspending dictation: {e}")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")

    def stop_nerd_dictation(self):
        """Stop nerd-dictation process."""
        if not self.dictation_process:
            return

        print("Stopping nerd-dictation...")
        cmd = [str(self.python_exe), str(self.nerd_dictation), "end"]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            # Try to kill the process if end command fails
            if self.dictation_process:
                self.dictation_process.terminate()

        self.dictation_process = None

    def on_press(self, key):
        """Handle key press events."""
        # Get the key name
        key_name = None
        if hasattr(key, "name"):
            key_name = key.name
        elif key == keyboard.Key.alt_r:
            key_name = "alt_r"
        elif key == keyboard.Key.alt_gr:
            key_name = "alt_gr"
        elif key == keyboard.Key.caps_lock:
            key_name = "caps_lock"
        elif key == keyboard.Key.menu:
            key_name = "menu"  # This is the "compose" or "menu" key

        # Check for double-tap on activation key
        if key_name == self.activation_key:
            current_time = time.time()
            last_tap = self.last_tap_time.get(key_name, 0)

            if current_time - last_tap <= self.double_tap_timeout:
                # Double tap detected!
                self.last_tap_time[key_name] = 0  # Reset to prevent triple-tap
                self.toggle_dictation()
            else:
                # First tap
                self.last_tap_time[key_name] = current_time

    def run(self):
        """Start the push-to-talk controller."""
        # Write PID file
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)
        self.pid_file.write_text(str(os.getpid()))

        try:
            # Start nerd-dictation in suspended state
            self.start_nerd_dictation()

            key_display = self.activation_key.replace("_", " ").title()
            print(f"\nHotkey ready. Double-tap {key_display} to start/stop dictation.")
            print("Press Ctrl+C to exit.")

            # Start listening for keyboard events
            with keyboard.Listener(on_press=self.on_press) as listener:
                try:
                    listener.join()
                except KeyboardInterrupt:
                    pass
        finally:
            # Cleanup
            print("\nCleaning up...")
            self.stop_nerd_dictation()

            # Remove PID file
            try:
                self.pid_file.unlink()
            except:
                pass

            print("Hotkey controller stopped.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Hotkey activation for nerd-dictation")
    parser.add_argument("--device", help="Audio device name (default: system default)")
    parser.add_argument(
        "--key",
        default="caps_lock",
        choices=["alt_r", "alt_gr", "caps_lock", "menu"],
        help="Key to double-tap for activation (default: caps_lock)",
    )

    args = parser.parse_args()

    if args.device:
        print(f"Using audio device: {args.device}")
    else:
        print("Using default audio input device")

    print(f"Activation key: double-tap {args.key.replace('_', ' ').title()}")

    controller = PushToTalkController(args.device, args.key)
    controller.run()


if __name__ == "__main__":
    main()
