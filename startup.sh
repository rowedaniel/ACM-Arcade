#!/bin/bash
# Boot PICO8 in carts/ directory
source .env
cd $PICO8_ROOT
$PICO8 -splore -home ./home -root_path ./carts -windowed 0 -draw_rect 80,0,480,480
