import atexit
import json
import time
from functools import partial
import inventorhatmini
import paho.mqtt.client as mqtt

last_message = 0
board = inventorhatmini.InventorHATMini()
left_motor = board.motors[1]
right_motor = board.motors[0]
pan = board.servos[0]
tilt = board.servos[1]

def set_servo_position(servo, client, userdata, msg, fine_tune=0):
    try:
        position = float(msg.payload) + fine_tune
        servo.value(position)
    except OSError:
        print("Error: Failed to set servo position")
    except ValueError:
        print("Error: Invalid position value")
    position = float(msg.payload)
    servo.value(position)

def stop_servo(servo, client=None, userdata=None, msg=None):
    if servo.is_enabled():
        servo.disable()

def all_messages(client, userdata, msg):
    global last_message
    last_message = time.time()
    print(f"{msg.topic} {msg.payload}")

def set_motor_wheels(client, userdata, msg):
    left, right = json.loads(msg.payload)
    left_motor.enable()
    left_motor.speed(left)
    right_motor.enable()
    right_motor.speed(right)

def stop_motors(client=None, userdata=None, msg=None):
    left_motor.stop()
    right_motor.stop()
    stop_servo(pan)
    stop_servo(tilt)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("motors/#")
    client.subscribe("leds/#")
    client.subscribe("all/#")

def exit_handler():
    stop_motors()
    board.leds.clear()

atexit.register(exit_handler)

mqtt_username = "robot"
mqtt_password = "robot"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect

client.message_callback_add("motors/#", all_messages)
client.message_callback_add("motors/stop", stop_motors)
client.message_callback_add("motors/wheels", set_motor_wheels)
client.message_callback_add("motors/servo/pan/position", partial(set_servo_position, pan, fine_tune=-5))
client.message_callback_add("motors/servo/pan/stop", partial(stop_servo, pan))
client.message_callback_add("motors/servo/tilt/position", partial(set_servo_position, tilt, fine_tune=6))
client.message_callback_add("motors/servo/tilt/stop", partial(stop_servo, tilt))
client.message_callback_add("all/stop", stop_motors)
client.message_callback_add("all/#", all_messages)

client.connect("localhost", 1883)
board.leds.set_rgb(0, 0, 255, 0)
client.loop_start()
while True:
    if time.time() - last_message > 1:
        stop_motors()
    time.sleep(0.1)
