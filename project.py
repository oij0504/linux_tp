import RPi.GPIO as GPIO
import time
from gpiozero import PWMOutputDevice
import adafruit_dht
import board

from time import sleep



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BUTTON = 24
LED = 23
TRIG = 13
ECHO = 19
GPIO.setup(LED, GPIO.OUT)

buzzer_pin = 12
pwm_device = PWMOutputDevice(pin=12, frequency=100, initial_value=0.5)

dht_device = adafruit_dht.DHT22(board.D4)

pwm_device.value = 0


GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


try :
    while True :
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

        GPIO.output(LED, GPIO.LOW)


        if temperature >= 30 or distance <= 10:
            GPIO.output(LED, GPIO.HIGH)
            pwm_device.frequency = 100
            pwm_device.value = 0.5
            sleep(0.5)
            pwm_device.value = 0


    

        print("Distance : ", distance, "cm", "temperature: ", temperature)

        
except :
    GPIO.cleanup()
    dht_device.exit()


