import subprocess
import os
import time
import logging
from inputs import get_gamepad
import threading

START_BTN = "BTN_BASE4"

# to avoid problems with startup
time.sleep(4)

logging.basicConfig(filename="screensaver.log", level=logging.INFO)
logger = logging.getLogger()

def get_winid(process):
    return subprocess.run(['xdotool', 'search', '--pid',  str(process.pid)], capture_output=True).stdout.strip()

def focus_window(winid, otherid):
    logger.info(f'switching to, {winid}, from {otherid}. time is {time.time()}')
    subprocess.run(['xdotool', 'windowmap', winid.decode('utf-8')])
    if otherid:
        subprocess.run(['xdotool', 'windowunmap', otherid.decode('utf-8')])

def start_program(cmd):
    p = subprocess.Popen(cmd)
    p_winid = None
    while not p_winid:
        time.sleep(0.1)
        p_winid = get_winid(p)
    return p, p_winid

def start_screensaver():
    screensaver, screensaver_winid = start_program(['/home/lcacm/Desktop/pico-8/pico8_64', '-run', '.lexaloffle/pico-8/carts/demos/dots3d.p8', '-windowed'])
    focus_window(screensaver_winid, game_winid)
    return screensaver, screensaver_winid

def resume_game(screensaver, screensaver_winid):
    focus_window(game_winid, screensaver_winid)
    time.sleep(0.3)
    screensaver.terminate()

# start game
#game,game_winid = start_program(['/home/lcacm/Desktop/pico-8/pico8_64', '-windowed', '-splore'])
game,game_winid = start_program(['/home/lcacm/launcharcade.sh'])

logger.info(f'game:{game_winid}')



# main loop
idletime = time.time()
IDLETHRESH = 3 
in_game = True

button_pressed = threading.Event()
pause_pressed = threading.Event()
# make a thread for monitoring button inputs
def read_events():
    logger.info('starting thread')
    while True:
        for event in get_gamepad():
            logger.info(f'got event {event}')
            if event.code == START_BTN:
                # in the screensaver, someone tried to pause
                pause_pressed.set()
            button_pressed.set()
def poll_gamepad():
    if button_pressed.is_set():
        if pause_pressed.is_set():
            # TODO: send unpause signal to PICO8
            pause_pressed.clear()
        button_pressed.clear()
        return True
    return False

            
button_thread = threading.Thread(target=read_events, daemon=True)
button_thread.start()

focus_window(game_winid, None)
while True:
    if in_game and time.time() - idletime > IDLETHRESH:
        logger.info("in game, switching to screensaver")
        screensaver, screensaver_winid = start_screensaver()
        in_game = False
    if poll_gamepad():
        if not in_game:
            logger.info("in screensaver, switching to game")
            resume_game(screensaver, screensaver_winid)
            in_game = True
        idletime = time.time()

