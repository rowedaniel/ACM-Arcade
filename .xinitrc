#!/bin/sh
xrandr --output HDMI-1 --mode 640x480 --rate 60

bash -c "cd /home/lcacm/Desktop/ACM-Arcade/ && ./.venv/bin/python run.py " &

/home/lcacm/dwm/dwm
