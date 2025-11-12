# Stop Dictation - Automator Quick Action

## Purpose
Stop voice dictation with a keyboard shortcut (⌘⇧X)

## Setup Instructions

1. **Open Automator**
   - Press `⌘ + Space` and type "Automator"
   - Or find in `/Applications/Automator.app`

2. **Create New Quick Action**
   - Click "New Document"
   - Select "Quick Action"
   - Click "Choose"

3. **Configure Workflow Settings** (top of window)
   - Workflow receives: `no input`
   - in: `any application`

4. **Add Run Shell Script Action**
   - Search for "Run Shell Script" in the left sidebar
   - Drag it to the workflow area
   - Set **Shell**: `/bin/zsh`
   - Set **Pass input**: `as arguments`

5. **Add Script Content**
   ```zsh
   #!/bin/zsh
   # Stop dictation
   export PATH="/usr/local/bin:$PATH"
   "$HOME/.config/nerd-dictation/vosk-end.sh" > /dev/null 2>&1
   
   # Optional: Show notification
   osascript -e 'display notification "⏹️ Dictation arrêtée / Stopped" with title "Nerd Dictation"'
   ```

6. **Save the Quick Action**
   - File → Save (⌘S)
   - Name: `Stop Dictation`
   - Location: `~/Library/Services/` (default)

7. **Assign Keyboard Shortcut**
   - Open **System Settings**
   - Go to **Keyboard** → **Keyboard Shortcuts** → **Services**
   - Scroll to "General" section
   - Find "Stop Dictation"
   - Click "Add Shortcut"
   - Press: `⌘⇧X` (Cmd+Shift+X)

## Testing

1. Start dictation first (`⌘⇧F` or `⌘⇧E`)
2. Speak some text
3. Press `⌘⇧X` to stop
4. You should see a notification confirming stop

## Troubleshooting

**Dictation doesn't stop?**
- Check if dictation is actually running: `ps aux | grep nerd-dictation`
- Try stopping manually: `~/.config/nerd-dictation/vosk-end.sh`
- Kill process if needed: `killall -9 nerd-dictation`

**Shortcut doesn't work?**
- Check System Settings → Privacy & Security → Accessibility
- Ensure Automator is allowed

**Script errors?**
- Open Console.app
- Filter for "Automator" to see error logs
