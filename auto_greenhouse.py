import datetime as dt
import time
import threading
import RPi.GPIO as GPIO
import Adafruit_DHT
import calendar
import logging
logging.basicConfig(filename='info.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' ,level=logging.INFO)
def temp_sensor():
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4

    humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    while humidity is None or temperature is None:
        humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
        print("Error reading temperature trying again in 10 seconds")
        time.sleep(10)
    logging.info("Temp is %s humidity is %s",temperature,humidity)
    return humidity,temperature

def setup_pins(pinlist):
    GPIO.setmode(GPIO.BCM)
    for i in pinlist:
        GPIO.setup(i,GPIO.OUT)
        GPIO.output(i,GPIO.HIGH)

def lights_on():
     weekday,hour,minute,second = get_time()
     print('Turning lights on at',hour,':',minute)
     logging.info("Lights Turned ON")
     GPIO.output(17,GPIO.LOW)
def lights_off():
    weeday,hour,minute,second = get_time()
    print('Turning lights off at',hour,':',minute)
    logging.info("Lights Turned OFF")
    GPIO.output(17,GPIO.HIGH)

def water_plant(ml):
    # 5 ml per secound
    num_seconds = ml / 5.5417
    print("Sending: ",ml, "ml or ",ml/1000,"L to Plant")
    print('Watering plant for  : ',num_seconds,' seconds')
    GPIO.output(27,GPIO.LOW)
    time.sleep(num_seconds)
    GPIO.output(27,GPIO.HIGH)
    print('Done Watering Plant')
    logging.info("Plant Watered with %s ml in %s seconds",ml,num_seconds)

def get_temp():
    return (temp,humid)
def get_time():
    current_time = dt.datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second
    weekday = calendar.day_name[current_time.weekday()]
    return weekday, hour,minute,second

def automatic_green(plant_name = None):
    weekday,hour,minute,second = get_time()
    # Test Starter
    lights_on()
    time.sleep(5)
    lights_off()
    plant_counter = 0
    while True:
        weekday, hour,minute,second = get_time()
        if (((minute == 30 ) & (second == 0)) | ((minute == 0 & second == 0))):
             humidity,temperature = temp_sensor()
             print("Humidity is :",humidity, "Temperature is : ",temperature)
        if ((hour == 7) & (minute == 0) & (second == 0)):
            lights_on()
        if ((hour == 12) & (minute == 0) & (second == 0)):
            lights_off()

        print(weekday,' ',hour,':',minute,':',second)
        if (((weekday == 'Monday') |  (weekday == "Wednesday")) & ((hour == 8) & (minute == 15) & (second == 0))):
            print("Watering Plant")
            start_auto_water = threading.Thread(target=water_plant,args=(30,))
            start_auto_water.start()

        time.sleep(1)

#pinlist = [17,27,22,23]
#setup_pins(pinlist)
#print("Testing initial")
#lights_on(None,None)
#time.sleep(3)
#lights_off(None,None)
#try:
#    while True:
#
#        time.sleep(1)
#        hour,minute,second = get_time()
#        print(hour,':',minute,':',second)
#        humidity,temperature = temp_sensor()
#        print('Temp={0:0.1f} C  Humidity={1:0.1f}%'.format(temperature,humidity))
#        if ((hour == 7) & (minute == 0) & (second == 0)):
#            lights_on(hour,minute)
#        if ((hour == 12) & (minute == 0) & (second == 0)):
#            lights_off(hour,minute)
#        if((hour == 12) & (minute == 49 ) & (second == 0)):
#            start_thred = threading.Thread(target=water_plant,args=(1000,))
#            start_thred.start()
    #    time.sleep(1)
#except KeyboardInterrupt:
#    print('Quit')
#    GPIO.cleanup()
#    print('GPIO CLEANED')
