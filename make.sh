#!/bin/bash
gcc -std=c99 -o set_fan_level set_fan_level.c
sudo chown root set_fan_level
sudo chmod u+s set_fan_level
