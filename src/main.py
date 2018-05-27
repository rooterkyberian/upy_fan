import machine
import utime as time


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke from a deep sleep')


SPEED = 0
motor_pin = machine.Pin(4)
motor_pwm = machine.PWM(motor_pin)
motor_pwm.freq(500)
motor_pwm.duty(SPEED)


def get_dht_sensor():
    import dht

    dht_sensor = dht.DHT11(machine.Pin(5))
    try:
        dht_sensor.measure()  # is it even connected?
    except OSError:
        dht_sensor = None
    return dht_sensor


dht_sensor = get_dht_sensor()


def get_mqtt_client():
    if not settings.BROKER:
        return None
    from umqtt.robust import MQTTClient
    client = MQTTClient(settings.NODE_ID, settings.BROKER)
    client.connect()

    print('MQTT client connected to broker', settings.BROKER)
    return client


mqtt_client = get_mqtt_client()


def main():
    pass
    #dht_sensor.measure()
    #print('Temp: %d' % dht_sensor.temperature())
    #print('Humidity: %d' % dht_sensor.humidity())


import gc


PUB_FAN_NEXT_TICK = 0
def publish_fan_state():
    mqtt_client.publish(
        settings.NODE_ID + settings.MQTT_FAN_SPEED,
        str(SPEED).encode(),
    )
    mqtt_client.publish(
        settings.NODE_ID + settings.MQTT_FAN_STATE,
        b'ON' if SPEED > 0 else b'OFF',
    )
    global PUB_FAN_NEXT_TICK
    PUB_FAN_NEXT_TICK = time.ticks_add(
        time.ticks_ms(),
        1000 * 30,
    )


PUB_SENSOR_NEXT_TICK = 0
def publish_sensor():
    dht_sensor.measure()
    mqtt_client.publish(
        settings.NODE_ID + settings.MQTT_SENSOR_HUMIDITY,
        str(dht_sensor.humidity()).encode(),
    )
    mqtt_client.publish(
        settings.NODE_ID + settings.MQTT_SENSOR_TEMP,
        str(dht_sensor.temperature()).encode(),
    )
    global PUB_SENSOR_NEXT_TICK
    PUB_SENSOR_NEXT_TICK = time.ticks_add(
        time.ticks_ms(),
        1000 * 30,
    )


def sub_cb(topic, msg):
    global SPEED
    try:
        SPEED = int(msg)
    except ValueError:
        SPEED = 0
        if msg == b'ON':
            SPEED = 1000
    motor_pwm.duty(SPEED)
    publish_fan_state()


mqtt_client.set_callback(sub_cb)
mqtt_client.subscribe(settings.NODE_ID + settings.MQTT_FAN_SPEED_SET)
mqtt_client.subscribe(settings.NODE_ID + settings.MQTT_FAN_STATE_SET)
print('subscribed')


try:
    publish_fan_state()
    publish_sensor()
except:
    pass


while True:
    tick = time.ticks_ms()
    try:
        mqtt_client.check_msg()
        if time.ticks_diff(PUB_FAN_NEXT_TICK, tick) <= 0:
            publish_fan_state()
        if dht_sensor and time.ticks_diff(PUB_SENSOR_NEXT_TICK, tick) <= 0:
            publish_sensor()
    except Exception as e:
        print(e)
        time.sleep(3)
    gc.collect()
