#!/usr/bin/python3
import os.path
import re
import signal
from subprocess import run, PIPE

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import GLib as glib
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

APPINDICATOR_ID = 'fanspeed_indicator'
REFRESH_RATE_MS = 2500

def run_stdout(command):
    return run(command, stdout=PIPE).stdout.decode('utf-8')

SENSORS_RX = re.compile(r'Package id 0: *\+(?P<temp_celsius>[0-9.]+).C')


def get_temperature():
    log = run_stdout(['sensors', 'coretemp-isa-0000'])
    match = SENSORS_RX.search(log)
    assert match is not None, log
    return float(match.groupdict()['temp_celsius'])


def set_fanspeed(speed):
    speed = str(speed)
    assert speed in {'0', '1', '2', '3', '4', '5', '6', '7',
                     'automatic', 'disengaged'}
    run(['./set_fan_level', speed])
    return


def menu_fanspeed_helper(menuitem, speed):
    if speed == 'maximum':
        speed = 'disengaged'
    set_fanspeed(speed)
    return True


def get_fanspeed():
    data = {}
    with open('/proc/acpi/ibm/fan', 'r') as fan:
        for line in fan:
            fields = [x for x in line.rstrip().split('\t') if len(x) > 0]
            data[fields[0].rstrip(':')] = fields[1]
    data['speed'] = int(data['speed'])
    assert 'status' in data
    assert 'level' in data
    # expect speed, status, level
    return data


def update_label(ind_app):
    speed = get_fanspeed()
    if speed['level'] == 'disengaged':
        speed['level'] = 'maximum'
    ind_app.set_label('%d\u00b0C %d rpm %s' % (get_temperature(), speed['speed'], speed['level'][0]), '')
    return True


def main():
    indicator = appindicator.Indicator.new(
            APPINDICATOR_ID,
            #gtk.STOCK_INFO,
            os.path.abspath('thermometer.svg'),
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    update_label(indicator)
    glib.timeout_add(REFRESH_RATE_MS, update_label, indicator)
    gtk.main()


def build_menu():
    menu = gtk.Menu()
    for level in ['automatic'] + list(range(0,8)) + ['maximum']:
        item = gtk.MenuItem('Level %s' % level)
        item.connect('activate', menu_fanspeed_helper, level)
        menu.append(item)
    quit_item = gtk.MenuItem('Quit')
    quit_item.connect('activate', quit)
    menu.append(quit_item)
    menu.show_all()
    return menu


def quit(_):
    notify.uninit()
    gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
