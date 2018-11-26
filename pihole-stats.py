#!/usr/bin/env python

import os
import sys
import time
import pihole as ph

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib
from luma.oled.device import sh1106
import RPi.GPIO as GPIO

from datetime import datetime
from luma.core.render import canvas
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# display configuration

serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)
device = sh1106(serial, rotate=2)

# pihole configuration

pihole = ph.PiHole("127.0.0.1")

# oled
def pihole_status():
    return " Status: " + pihole.status

def pihole_queries():
    return " DNS Queries: " + pihole.queries

def pihole_blocked_queries():
    return " Blocked: " + pihole.blocked + " (" + pihole.ads_percentage + "%)"

def pihole_blocked_domains():
    return " Blocklist: " + pihole.domain_count

def stats(pihole):
    # use custom font
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.rectangle((0, 12, 127, 0), outline="white", fill="white")
        draw.text((10, 0), "Pi Hole Statistics", fill="black")
        draw.text((0, 14), pihole_status(), font=font2, fill="white")
        draw.text((0, 26), pihole_queries(), font=font2, fill="white")
        draw.text((0, 38), pihole_blocked_queries(), font=font2, fill="white")
        draw.text((0, 50), pihole_blocked_domains(), font=font2, fill="white")
def main():
    while True:
        pihole.refresh()
        stats(pihole)
        time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
	pass
