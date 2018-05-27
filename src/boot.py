# This file is executed on every boot (including wake-boot from deepsleep)
import webrepl
import utime as time


import settings


def do_connect():
    import network

    pw = settings.WIFI_PASS

    ap_if = network.WLAN(network.AP_IF)
    ap_if.config(essid=settings.NODE_ID, password=pw)
    # print('access point Polly open')

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        # print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(settings.WIFI_SSID, pw)
        while not sta_if.isconnected():
            pass
    print('connected at:', sta_if.ifconfig())


do_connect()

#webrepl.start(password=settings.WEBREPL_PASS)
time.sleep(1)
print('Booted!')
