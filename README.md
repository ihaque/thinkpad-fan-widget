GTK application indicator widget for core temperature and fanspeed on Thinkpads

# Setup

## Fan control and temperature sensors

You must enable the option in the `thinkpad_acpi` driver to allow fan speed control,
and you must install the `lm-sensors` package and set up the coretemp driver. Then
reboot.

```
sudo sh -c "echo 'options thinkpad_acpi fan_control=1' > /etc/modprobe.d/thinkpad_acpi.conf"
sudo chown root:root /etc/modprobe.d/thinkpad_acpi.conf
sudo chmod 644 /etc/modprobe.d/thinkpad_acpi.conf

sudo apt install lm-sensors
sudo sensors-detect

sudo reboot
```

## Python environment

This uses the system installation of Python 3, though you could run it in a virtualenv if you
wanted.

```
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 libappindicator3-dev
```

## Build the binary

This widget uses a setuid binary to poke the fan speed in `/proc/acpi/ibm/fan` The widget itself
does not run with elevated permissions, and the binary is pretty minimal; you can read the source
yourself to verify.

```
./make.sh
```


# To run

Assuming you're running using the system Python,

```
/usr/bin/python3 widget.py
```
