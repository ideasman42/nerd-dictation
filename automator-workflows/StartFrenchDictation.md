# Start French Dictation - Automator Quick Action

## Purpose
Launch French voice dictation with a keyboard shortcut (⌘⇧F)

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
   # Start French dictation with VOSK
   export PATH="/usr/local/bin:$PATH"
   "$HOME/.config/nerd-dictation/vosk-fr.sh" > /dev/null 2>&1 &
   
   # Optional: Show notification
   osascript -e 'display notification "🇫🇷 Dictation française activée" with title "Nerd Dictation"'
   ```

6. **Save the Quick Action**
   - File → Save (⌘S)
   - Name: `Start French Dictation`
   - Location: `~/Library/Services/` (default)

7. **Assign Keyboard Shortcut**
   - Open **System Settings**
   - Go to **Keyboard** → **Keyboard Shortcuts** → **Services**
   - Scroll to "General" section
   - Find "Start French Dictation"
   - Click "Add Shortcut"
   - Press: `⌘⇧F` (Cmd+Shift+F)

## Testing

1. Press `⌘⇧F` in any application
2. You should see a notification
3. Start speaking in French
4. Text should appear where your cursor is

## Troubleshooting

**Shortcut doesn't work?**
- Check System Settings → Privacy & Security → Accessibility
- Ensure Automator and your terminal app are allowed

**No text appears?**
- Check microphone permissions
- Verify the script path is correct
- Test manually: `~/.config/nerd-dictation/vosk-fr.sh`

**Script errors?**
- Open Console.app
- Filter for "Automator" to see error logs
