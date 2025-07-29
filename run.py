import subprocess
import os
import signal
import time
import logging
from inputs import get_gamepad
import threading

START_BTN = "BTN_BASE4"

logging.basicConfig(filename="screensaver.log", level=logging.INFO)
logger = logging.getLogger()

def get_winid(pid):
    return subprocess.run(['xdotool', 'search', '--pid',  str(pid)], capture_output=True).stdout.strip()

def focus_window(winid, otherid):
    logger.info(f'switching to, {winid}, from {otherid}. time is {time.time()}')
    subprocess.run(['xdotool', 'windowmap', winid.decode('utf-8')])
    if otherid:
        subprocess.run(['xdotool', 'windowunmap', otherid.decode('utf-8')])

def start_program(cmd):
    try:
        prog_pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, preexec_fn=os.setsid)
        pico_pid = int(prog_pid.stdout.readline().strip())
        logger.info(f'got pid: {pico_pid}')
        p_winid = None
        while not p_winid:
            time.sleep(0.1)
            p_winid = get_winid(pico_pid)
        return prog_pid, p_winid
    except Exception as e:
        logger.info(f'got error: {e}')

def start_screensaver(game_winid):
    screensaver, screensaver_winid = start_program(['./screensaver.sh'])
    focus_window(screensaver_winid, game_winid)
    return screensaver, screensaver_winid

def resume_game(screensaver, screensaver_winid, game_winid):
    focus_window(game_winid, screensaver_winid)
    time.sleep(0.3)
    os.killpg(os.getpgid(screensaver.pid), signal.SIGTERM)
    #screensaver.terminate()

def main():

    # to avoid problems with startup
    time.sleep(4)

    # start game
    logger.info('starting game')
    game,game_winid = start_program(['./startup.sh'])

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
            screensaver, screensaver_winid = start_screensaver(game_winid)
            in_game = False
        if poll_gamepad():
            if not in_game:
                logger.info("in screensaver, switching to game")
                resume_game(screensaver, screensaver_winid, game_winid)
                in_game = True
            idletime = time.time()

if __name__ == "__main__":
    main()
