from time import sleep
import paho.mqtt.client as mqtt
import adafruit_dht
import board
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BUTTON = 24
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

MY_ID = "01"

ECHO = 19
TRIG = 13

dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)



MQTT_HOST = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = f"mobile/{MY_ID}/sensing"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

try:
    while True:
        if GPIO.input(BUTTON) == True:
            GPIO.setup(TRIG, GPIO.OUT)
            GPIO.setup(ECHO, GPIO.IN)
            GPIO.output(TRIG, False)
            time.sleep(0.5)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0 :
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1 :
                pulse_end = time.time()
 
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            distance = round(distance, 2)
            temperature = dht_device.temperature
            value = f'{{"temperature": {temperature:.1f}, "distance": {distance}}}'
            client.publish(MQTT_TOPIC, value)
            print(value)            
except KeyboardInterrupt:
    print("종료합니다!!")
finally:
    client.loop_stop()
    client.disconnect()