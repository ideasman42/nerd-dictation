#!/usr/bin/env python3

import os

COMMANDS = {}

def register_command(command, action):
    COMMANDS[command] = action

def execute_command(command):
    if command in COMMANDS:
        COMMANDS[command]()
    else:
        print(f"Unknown command: {command}")

def open_firefox():
    os.system("firefox")

def open_terminal():
    os.system("gnome-terminal")

register_command("open firefox", open_firefox)
register_command("open terminal", open_terminal)

def move_mouse_up():
    from pynput.mouse import Controller, Button
    mouse = Controller()
    mouse.move(0, -10)

def move_mouse_down():
    from pynput.mouse import Controller, Button
    mouse = Controller()
    mouse.move(0, 10)

def move_mouse_left():
    from pynput.mouse import Controller, Button
    mouse = Controller()
    mouse.move(-10, 0)

def move_mouse_right():
    from pynput.mouse import Controller, Button
    mouse = Controller()
    mouse.move(10, 0)

def mouse_click():
    from pynput.mouse import Controller, Button
    mouse = Controller()
    mouse.click(Button.left, 1)

register_command("mouse up", move_mouse_up)
register_command("mouse down", move_mouse_down)
register_command("mouse left", move_mouse_left)
register_command("mouse right", move_mouse_right)
register_command("mouse click", mouse_click)

def select_all():
    from pynput.keyboard import Controller, Key
    keyboard = Controller()
    with keyboard.pressed(Key.ctrl):
        keyboard.press('a')
        keyboard.release('a')

def copy_selection():
    from pynput.keyboard import Controller, Key
    keyboard = Controller()
    with keyboard.pressed(Key.ctrl):
        keyboard.press('c')
        keyboard.release('c')

def paste_selection():
    from pynput.keyboard import Controller, Key
    keyboard = Controller()
    with keyboard.pressed(Key.ctrl):
        keyboard.press('v')
        keyboard.release('v')

register_command("select all", select_all)
register_command("copy", copy_selection)
register_command("paste", paste_selection)

def switch_application():
    from pynput.keyboard import Controller, Key
    keyboard = Controller()
    with keyboard.pressed(Key.alt):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)

def switch_window():
    from pynput.keyboard import Controller, Key
    keyboard = Controller()
    with keyboard.pressed(Key.alt):
        keyboard.press('`')
        keyboard.release('`')

register_command("switch application", switch_application)
register_command("switch window", switch_window)
