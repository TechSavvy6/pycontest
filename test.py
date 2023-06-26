from pynput.mouse import Controller
from pynput.keyboard import Key, Controller as KeyboardController
from time import sleep, time
import random
import os
import logging
import sys
import subprocess
import re

mouse = Controller()
keyboard = KeyboardController()

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def get_active_window_title():
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        return match.group("name").strip(b'"').decode("utf-8")                                                                                                                                                                                                                                                                                          

    return None                                                                                                                                                                                                 

def get_active_window():
    import sys
    active_window_name = None
    if sys.platform in ['linux', 'linux2']:
        # Alternatives: https://unix.stackexchange.com/q/38867/4784
        # try:
        #     import wnck
        # except ImportError:
        #     logging.info("wnck not installed")
        #     wnck = None
        # if wnck is not None:
        #     screen = wnck.screen_get_default()
        #     screen.force_update()
        #     window = screen.get_active_window()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        #     if window is not None:
        #         pid = window.get_pid()
        #         with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
        #             active_window_name = f.read()
        # else:
        #     try:
        #         from gi.repository import Gtk, Wnck
        #         gi = "Installed"
        #     except ImportError:
        #         logging.info("gi.repository not installed")
        #         gi = None
        #     if gi is not None:
        #         Gtk.init([])  # necessary if not using a Gtk.main() loop
        #         screen = Wnck.Screen.get_default()
        #         screen.force_update()  # recommended per Wnck documentation
        #         active_window = screen.get_active_window()
        #         pid = active_window.get_pid()
        #         with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
        #             active_window_name = f.read()

        active_window_name = get_active_window_title()
    elif sys.platform in ['Windows', 'win32', 'cygwin']:
        # https://stackoverflow.com/a/608814/562769
        import win32gui
        window = win32gui.GetForegroundWindow()
        
        active_window_name = win32gui.GetWindowText(window)
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        # https://stackoverflow.com/a/373310/562769
        from AppKit import NSWorkspace
        active_window_name = (NSWorkspace.sharedWorkspace()
                              .activeApplication()['NSApplicationName'])
    else:
        print("sys.platform={platform} is unknown. Please report."
              .format(platform=sys.platform))
        print(sys.version)
    return active_window_name

def smooth_interval_sleep(base = 0.03, unit = 0.01, variation = 8):
    sleep_delta = random.randrange(0, variation) * unit + base
    sleep(sleep_delta)

def mouse_scroll_action():
    direction = random.randint(0, 10) % 2
    if (direction == 0):
        direction = -1

    moves = random.randint(3, 8)

    for x in range(moves):
        mouse.scroll(0, 1 * direction)
        smooth_interval_sleep()

def keyboard_move_action(min = 5, max = 15):
    direction = random.randint(0, 1000) % 4
    
    if direction == 0:
        moves = random.randint(min, max)
        for x in range(moves):
            keyboard.tap(Key.down)
            smooth_interval_sleep(0.25, 0.02, 8)
    elif direction == 1:
        moves = random.randint(min, max)
        for x in range(moves):
            keyboard.tap(Key.up)
            smooth_interval_sleep(0.25, 0.02, 8)
    # elif direction == 2:
    #     moves = random.randint(min, max)
    #     for x in range(moves):
    #         keyboard.tap(Key.right)
    #         smooth_interval_sleep(0.25, 0.02, 8)
    else:
        moves = random.randint(0, 3)
        for x in range(moves):
            keyboard.tap(Key.left)
            smooth_interval_sleep(0.25, 0.02, 8)

def code_change_file():
    moves = random.randint(1, 10)
    keyboard.press(Key.ctrl)
    with keyboard.pressed(Key.ctrl):
        for x in range(moves):
            keyboard.tap('p')
            smooth_interval_sleep(0.1, 0.05, 7)
        keyboard.release(Key.ctrl)
    keyboard.release(Key.ctrl)

def change_window():
    moves = random.randint(1, 4)
    keyboard.press(Key.alt)
    with keyboard.pressed(Key.alt):
        for x in range(moves):
            keyboard.tap(Key.tab)
            smooth_interval_sleep(0.3, 0.05, 3)
        keyboard.release(Key.alt)
    keyboard.release(Key.alt)

def do_some_action(wName):
    if 'visual studio code' in wName:
        choice = random.randint(0, 1000) % 4
        if choice == 0:
            keyboard_move_action()
        elif choice == 1:   
            mouse_scroll_action()
        elif choice == 2:
            code_change_file()
            choice = random.randint(0, 1000) % 2
            if choice == 0:
                keyboard_move_action()
            else:
                mouse_scroll_action()
        else:   
            change_window()
    elif 'google chrome' in wName:
        choice = random.randint(0, 1000) % 2
        if choice == 0:
            mouse_scroll_action()
        else:
            change_window()
    else:
        change_window()

minutes = 422

start_time = time()
print(start_time)

while True:
    current_time = time()
    time_passed = current_time - start_time
    print(current_time - start_time)
    if time_passed > minutes * 60:
        break

    wName = get_active_window().lower()
    print("Active window: %s" % str(wName))

    dice = random.randint(0, 10)

    if dice > 7:
        continue

    do_some_action(wName)
    
    delta = random.randint(0, 30)

    sleep(20 + delta)


