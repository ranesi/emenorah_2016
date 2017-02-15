import RPi.GPIO as GPIO
import time

'''
    eMenorah v0.3a
    --NOTE--
    Current release only works for the 2016-2017 holiday season.
    C-Language Version forthcoming.
    Required modules:
        -RPi.GPIO
'''

#ledList = [2,3,4,17,27,22,10,9,11] #GPIO pinouts
ledList = [3,5,7,11,13,15,19,21,23] #pin number
toggle = 1

def init():
    '''Procedure run to initialize RPi.GPIO.'''
    #GPIO.setmode(GPIO.BCM)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(40,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    initLED()

def initLED():
    counter = 0
    while counter < 9:
        allOff()
        on(ledList[counter])
        time.sleep(0.1)
        counter += 1
    allOff()

def on(x):
    '''Turns on (x) LED.'''
    GPIO.setup(x,GPIO.OUT)
    GPIO.output(x,GPIO.LOW)

def off(x):
    '''Turns off (x) LED.'''
    GPIO.setup(x,GPIO.OUT)
    GPIO.output(x,GPIO.HIGH)

def allOff():
    for led in ledList:
        off(led)

def shutdown():
    '''Shutdown all LEDs and perform cleanup.'''
    allOff()
    GPIO.cleanup()

def light(x):
    '''Activates (x) lights in sequence.'''
    on(ledList[0]) #central candle always on
    y = 1
    while y < x + 1:
        on(ledList[y])
        y+=1

def power(ev=None):
    global toggle
    toggle = not toggle
    if toggle == 1:
        getCandles()
    else:
        allOff()

def main():
    GPIO.add_event_detect(40, GPIO.FALLING, callback=power)
    while True:
        time.sleep(5) #necessary to prevent 100% CPU consumption
        pass

def getCandles():
    '''Retrieves local time, compares it, determines number of "candles"
       to send to light().'''
    today = time.localtime()
    candles = 0
    allOff()
    if today[0] == 2016 or today[0] == 2017:
        if today[1] == 12 or today[1] == 1:
            if today[2] == 24:
                if today[3] >= 17:
                    candles = 1
            elif today[2] >= 25:
                days = 25
                candles = 1
                while days <= 31:
                    if today[2] == days:
                        if today[3] >= 17:
                            candles+=1
                            break
                        break
                    candles+=1
                    days+=1
            elif today[1] == 1 and today[2] == 1:
                candles = 8
                if today[3] >= 17:
                    candles = 0
        if candles > 0:
            light(candles)

if __name__=='__main__':
    init()
    try:
        main()
    except KeyboardInterrupt:
        shutdown()
