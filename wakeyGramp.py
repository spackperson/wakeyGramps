import network
import time
import ntptime
from time import localtime
from machine import Pin

#functions
def resetLEDS():
    LED1.value(0)
    LED2.value(0)
    LED3.value(0)
    LED4.value(0)
    LED5.value(0)

#initialize lists and variables
LED1 = Pin(10, Pin.OUT)
LED2 = Pin(11, Pin.OUT)
LED3 = Pin(14, Pin.OUT)
LED4 = Pin(15, Pin.OUT)
LED5 = Pin(9, Pin.OUT)

resetLEDS()


# Replace with your Wi-Fi credentials
ssid = ""
password = ""

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
max_attempts = 10
attempt = 0
while not wlan.isconnected() and attempt < max_attempts:
    print("Connecting to Wi-Fi...")
    time.sleep(1)
    attempt += 1

if wlan.isconnected():
    LED1.value(1)
    print("Connected to Wi-Fi")
    
else:
    print("Failed to connect to Wi-Fi")
    
# Sync time from NTP server
ntptime.settime()

#create utc_offset for mountain time
UTC_OFFSET = -7 * 60 * 60

while True:


# Get the current time in UTC
    current_time = localtime()  # Returns a tuple in the format (year, month, day, hour, minute, second, weekday, yearday)

# Adjust UTC time to mountain time, accounting for Daylight savings
    mountain_time = localtime(time.time() + UTC_OFFSET)
# Print the current UTC time

    print("Current UTC time:", current_time)
    print("Current Mountain time:", mountain_time)
    if mountain_time[3] > 8:
        LED5.value(1)
        time.sleep(.5)
        LED5.value(0)
        time.sleep(.5)
        LED5.value(1)
        time.sleep(.5)
        LED5.value(0)
        time.sleep(.5)
        LED5.value(1)
    else:
        LED5.value(0)
    time.sleep(10)

