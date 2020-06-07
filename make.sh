#!/bin/bash
gcc -std=c99 -o set_fan_level set_fan_level.c
sudo chown root set_fan_level
sudo chmod u+s set_fan_level
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 libappindicator3-dev
