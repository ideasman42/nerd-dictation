# Automator Quick Actions for Nerd Dictation

This directory contains setup guides for creating macOS Automator Quick Actions to control voice dictation via keyboard shortcuts.

## Quick Actions Available

| Quick Action | Shortcut | Description |
|--------------|----------|-------------|
| 🇫🇷 Start French Dictation | `⌘⇧F` | Launch French voice dictation with full VOSK model |
| 🇬🇧 Start English Dictation | `⌘⇧E` | Launch English voice dictation with full VOSK model |
| ⏹️ Stop Dictation | `⌘⇧X` | Stop active dictation session |

## Setup Instructions

Follow the detailed guides in this directory:

1. **[StartFrenchDictation.md](./StartFrenchDictation.md)** - French dictation setup
2. **[StartEnglishDictation.md](./StartEnglishDictation.md)** - English dictation setup
3. **[StopDictation.md](./StopDictation.md)** - Stop dictation setup

Each guide includes:
- Step-by-step Automator configuration
- Shell script content
- Keyboard shortcut assignment
- Troubleshooting tips

## Prerequisites

Before setting up Automator Quick Actions, ensure you have:

- ✅ PulseAudio installed (`brew install pulseaudio`)
- ✅ Full VOSK models downloaded and extracted
- ✅ Launch scripts created in `~/.config/nerd-dictation/`
- ✅ Microphone permissions granted to Terminal/iTerm
- ✅ Accessibility permissions for Automator

## Benefits

### Without Automator (Manual)
```bash
# Start dictation
~/.config/nerd-dictation/vosk-fr.sh

# Stop dictation  
~/.config/nerd-dictation/vosk-end.sh
```

### With Automator (Keyboard Shortcuts)
- Press `⌘⇧F` to start French dictation
- Press `⌘⇧X` to stop
- Works from **any application**
- No terminal required
- Visual notifications

## Complete Documentation

For the full setup guide with SOCA Pulse optimization methodology, see:

📄 **[macOS Setup Guide](../docs/macos-setup-guide.html)** - Open in a browser for the complete interactive guide

## Permissions Required

### System Settings → Privacy & Security

1. **Microphone**
   - Terminal.app or iTerm.app
   - Automator

2. **Accessibility**  
   - Automator
   - Terminal.app or iTerm.app

3. **Automation** (if prompted)
   - Allow Automator to control System Events

## Troubleshooting

### Shortcuts not working?
- Check System Settings → Keyboard → Keyboard Shortcuts → Services
- Verify Quick Actions are in `~/Library/Services/`
- Log out and back in

### No notification appears?
- Check notification permissions for Automator
- Test script manually in Terminal

### Wrong language activates?
- Ensure you're using the correct shortcut
- Stop current session before starting a new language

## SOCA Pulse Integration

These Quick Actions are designed to integrate with the SOCA Pulse optimization methodology:

- **Iterative Refinement**: Quick start/stop enables rapid testing
- **Context Switching**: Instant language switching for bilingual workflows  
- **Fail-Closed**: Stop immediately when accuracy drops
- **Feedback Loop**: Visual notifications confirm state changes

## Contributing

Improvements and additional workflows welcome! Consider:

- Additional language support
- Custom notification sounds
- Status bar integration
- Alfred/Raycast workflows

## License

Same as parent project (Apache 2.0)
