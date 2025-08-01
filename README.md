# Lewis & Clark ACM Arcade

This is a collection of utilities for the LC ACM arcade machine!

Presently does not include automatic updating of games.
Games can be updated using (from inside this directory):
```sh
git submodule update --recursive
./.venv/bin/python build_games.py
```

## On the Rasberry PI at LC
- Automatically boots directly into pico8.
  - to quit, plug in a keyboard and press alt+shift+q
- Presently set to go to screensaver mode after 5 minutes of inactivity.

## If you need to access a gui application on the Raspberry PI:
After the boot process is finished and pico8 has started, press alt+shift+q
to leave the x session. Then, modify `~/.xinitrc`, commenting out the `bash` line.
It should look like this:
```sh
#!/bin/sh
xrandr --output HDMI-1 --mode 640x480 --rate 60

#bash -c "cd /home/lcacm/Desktop/ACM-Arcade/ && ./.venv/bin/python run.py " &

/home/lcacm/dwm/dwm
```
Finally, run `startx` to re-enter the graphical mode.
From here, you can press alt+p, followed by the program you want to run (e.g. `firefox`).
Press enter to confirm.
Note that it is configured to not display anything, so you will have no feedback as to whether it's
working until you press enter.
