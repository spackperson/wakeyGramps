import network
import time
import ntptime
from time import localtime, sleep
from machine import Pin

#debug print
print("Starting program...")

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

#initiate button

butPin = 20
myButton = Pin(butPin, Pin.IN, Pin.PULL_UP)
butStateNow = 1
butStateOld = 1
gameState = False

# Replace with your Wi-Fi credentials
ssid = ""
password = ""

# Reset LEDs initially
resetLEDS()

#Initialize Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(False) #start with wifi off

print("Entering main loop")

while True:
    #Debug - Print button state to verify reading
    #print("Button value:", myButton.value())
    
    #button handling
    butStateNow = myButton.value()
    
    #Button Toggle Logic
    if butStateNow == 1 and butStateOld == 0:#Reminder: 1 = button not being pressed, 0 = button is being pressed
        gameState = not gameState
        print("Game state:", gameState)
               
        #Toggle on/off actions
        if gameState:
            resetLEDS()
            #Connect to wi-fi if not already connected
            if not wlan.isconnected():
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
                    try:
                        # Sync time from NTP server
                        ntptime.settime()
                        print("Time synchonized")
                    except Exception as e: #e is a variable that stores the specific error thrown
                        print("Failed to sync time", e)
                else:
                    print("Failed to connect to Wi-Fi")
        else:
            #turn off actions
            resetLEDS()
            wlan.active(False)
            print("Wifi turned off")
        
    #Time Checking (only if gameState is True)
    if gameState and wlan.isconnected():
        #create utc_offset for mountain time
        UTC_OFFSET = -6 * 60 * 60
        
        #Get the current time in UTC
        current_time = localtime()  # Returns a tuple in the format (year, month, day, hour, minute, second, weekday, yearday)

        # Adjust UTC time to mountain time, accounting for Daylight savings
        mountain_time = localtime(time.time() + UTC_OFFSET)
        
        # Print the current UTC time
        print("Current UTC time:", current_time)
        print("Current Mountain time:", mountain_time)
        
        # check if it's after 9 in mountain time
        if mountain_time[3] > 9:
            LED5.value(1)
        else:
            LED5.value(0)
            LED1.valude(1)
            
    butStateOld = butStateNow #update button state
    sleep(.1) # Small delay to prevent button bounce





