# pounce code golf on a microprocessor

import board
import neopixel
import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

SEND_RATE = 10  # how often in seconds to send text

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

bright = 0.5
pixels = neopixel.NeoPixel(board.D5, 20, brightness=0.3)

from pounce import runtime
from pounce import parser
# [i t] [    t i + 20 % 10 - abs 5 *    ] pounce
cf = parser.parse("[1 + 127 *] [conv] compose")
cfr = runtime.purr(cf)

pr = parser.parse("[i t] [i 10 / t 5 / + sin] pounce 1 + 127 *")
pg = parser.parse("[i t] [i 10 / t 5 / - sin] pounce 1 + 127 *")
pb = parser.parse("[i t] [i 10 / t 5 / + cos] pounce 1 + 127 *")
next_report_t = 0
report_inter = 50

def it(i, t):
    global next_report_t, report_inter
    red = runtime.purr([i, t]+pr)[0]
    green = runtime.purr([i, t]+pg)[0]
    blue = runtime.purr([i, t]+pb)[0]
    if t > next_report_t:
        next_report_t = t + report_inter
        print(i, t, " -> ", red, green, blue)
    return [red, green, blue]

newCode = ""
while True:
    print("WAITING FOR BLE ...")
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        for i in range(0, 20):
            pixels[i] = it(i , time.monotonic())

    # Connected
    ble.stop_advertising()
    print("CONNECTED")

    # Loop and read packets
    # last_send = time.monotonic()
    # i t 3 / + sin 2 / 1 - b
    while ble.connected:
        line = uart_server.readline()
        if line:
            print(line[-2:-1].decode('utf-8'))
            print(line[-2:-1].decode('utf-8') == ",")
            if line[-2:-1].decode('utf-8') == ",":
                newCode += line[0:-2].decode('utf-8')
                print("building newCode : ", newCode)
            else:
                newCode += line[0:-3].decode('utf-8')
                colorCode = line[-2:-1].decode('utf-8')
                uart_server.write("[i t] [" + newCode + "] pounce\n")
                print("[i t] [" + newCode + "] pounce\n")
                uart_server.write("colorCode = " + colorCode + "\n")
                print("colorCode = " + colorCode + "\n")
                if colorCode == "r":
                    pr = parser.parse("[i t] [" + newCode + " 1 + 127 *] pounce")
                if colorCode == "g":
                    pg = parser.parse("[i t] [" + newCode + " 1 + 127 *] pounce")
                if colorCode == "b":
                    pb = parser.parse("[i t] [" + newCode + " 1 + 127 *] pounce")
                newCode = ""
        for i in range(0, 20):
            pixels[i] = it(i , time.monotonic())

    # Disconnected
    print("DISCONNECTED")
    
