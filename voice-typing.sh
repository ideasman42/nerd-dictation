#!/bin/bash
# Toggle nerd-dictation voice typing on/off.
#
# First call:  start daemon (loads model) and begin recording.
# Second call: kill the process (manual exit with notification).
# With --continuous + timeout: auto-suspends after silence, next call resumes.
#
# Bind this script to a hotkey (e.g. Super+H) in your desktop environment.
#
# Dependencies: parec (pulseaudio-utils), ydotool, wl-copy (wl-clipboard),
#               sherpa-onnx (pip install sherpa-onnx) or vosk (pip install vosk).
export YDOTOOL_SOCKET="/run/user/$(id -u)/.ydotool_socket"
NVIDIA_LIB="$HOME/.local/lib/python3.13/site-packages/nvidia"
export LD_LIBRARY_PATH="$NVIDIA_LIB/curand/lib:$NVIDIA_LIB/cufft/lib:$NVIDIA_LIB/nvjitlink/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
NERD_DICTATION="$HOME/Codes/VoiceTyping/nerd-dictation/nerd-dictation"
MODEL_DIR="$HOME/Codes/VoiceTyping/vosk-models/sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20"

PID=$(pgrep -f "nerd-dictation begin" | head -1)

if [ -z "$PID" ]; then
    notify-send -t 3000 -u critical "Voice Typing" "Loading model..."
    "$NERD_DICTATION" begin \
        --engine=sherpa \
        --vosk-model-dir="$MODEL_DIR" \
        --simulate-input-tool=YDOTOOL_CLIPBOARD \
        --continuous \
        --timeout=3 &
else
    STATE=$(awk '/^State:/{print $2}' /proc/"$PID"/status 2>/dev/null)
    if [ "$STATE" = "T" ]; then
        kill -CONT "$PID"
        notify-send -t 1500 -u low "Voice Typing" "Recording"
    else
        kill "$PID"
        notify-send -t 3000 -u critical "Voice Typing" "Manually killed (not timeout)"
    fi
fi
