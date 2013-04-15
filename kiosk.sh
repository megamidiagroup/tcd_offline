#!/bin/bash

width=`xrandr | grep \* | head -n1 | cut -d' ' -f4 | cut -d'x' -f1`
height=`xrandr | grep \* | head -n1 | cut -d' ' -f4 | cut -d'x' -f2`

xscreensaver -nosplash &
xmodmap -e 'keycode 67 = 0x0000' #disables F1
xmodmap -e 'keycode 37 = 0x0000' #disables Ctrl_L
xmodmap -e 'keycode 105 = 0x0000' #disables Ctrl_R
xmodmap -e 'keycode 64 = 0x0000' #disables Alt_L
xmodmap -e 'keycode 108 = 0x0000' #disables Ctrl_R
xmodmap -e 'keycode  67 = F1 XF86_Switch_VT_2' #hability F1 para Ctrl + Alt + F2
xsetroot -cursor_name left_ptr
while true; do /usr/bin/firefox http://localhost/loading.html -width $width -height $height; sleep 5s; done