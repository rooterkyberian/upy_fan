# upy_fan
micropython fan controller


# Hardware

* Wemos D1
* DHT11 temperature-humidity sensor
* Equation IR controlled fan (the IR daughter board with button has been replaced with Wemos D1)

It is important that the fan was originally controlled by IR remote, because it meant it had solid state variable speed control.
After testing it with multimeter it appeared the daughter board controlled main motor with signal varying from 2 to 5V (max speed).

# Environment setup

    pipenv install
    
# Configure

    cp src/settings.py.example src/settings.py

# Upload firmware
    
    make erase  # just to be safe
    make flash
    
# Upload code

    make upload

## References

Wemos D1 pinout:
https://escapequotes.net/esp8266-wemos-d1-mini-pins-and-diagram/

DHT11
https://nodemcu.readthedocs.io/en/master/en/modules/dht/#dhtread11
https://akizukidenshi.com/download/ds/aosong/DHT11.pdf

### Example Home Assistant configuration

    fan:
      - platform: mqtt
        name: attic_fan
        state_topic: "9aa71500/fan/state"
        command_topic: "9aa71500/fan/state@set"
        speed_state_topic: "9aa71500/fan/speed"
        speed_command_topic: "9aa71500/fan/speed@set"
        payload_low_speed: "0"
        payload_medium_speed: "250"
        payload_high_speed: "1000"
    sensor:
      - platform: mqtt
        name: "Temperature"
        state_topic: "9aa71500/sensor/temp"
        unit_of_measurement: '°C'
      - platform: mqtt
        name: "Humidity"
        state_topic: "9aa71500/sensor/humidity"
        unit_of_measurement: '%'

    # https://www.home-assistant.io/components/mqtt/
    mqtt:

### Handy commands for testing

    mosquitto_pub -h test.mosquitto.org -t '9aa71500/fan/speed@set' -m 0
    mosquitto_sub -h test.mosquitto.org -t '9aa71500/sensor/temp'
