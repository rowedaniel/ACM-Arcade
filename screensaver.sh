#!/bin/bash
# Boot PICO8 screensaver in carts/ directory
source .env
$PICO8 -run '~/.lexaloffle/pico-8/carts/demos/dots3d.p8' -windowed 0 -draw_rect 80,0,480,480 &
echo $!
