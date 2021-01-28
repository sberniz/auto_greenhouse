
from flask import Flask, render_template,escape,request
import RPi.GPIO as GPIO
import threading
import os
import signal
import atexit
import logging
from auto_greenhouse.auto_greenhouse import lights_on,lights_off, water_plant,get_time,automatic_green

def setup_pins(pinlist):
    GPIO.setmode(GPIO.BCM)
    for i in pinlist:
        GPIO.setup(i,GPIO.OUT)
        GPIO.output(i,GPIO.HIGH)


pinlist = [17,27,22,23]
setup_pins(pinlist)
start_thred2 = threading.Thread(target=automatic_green,args=(None,))
start_thred2.start()


def cleanup_pins():
    GPIO.cleanup()
    print("Cleaned GPIO")
atexit.register(cleanup_pins)

#def create_app():
app = Flask(__name__)
@app.route('/')
def root():

    message_button = ""
    color = ""
    call = ""
    status = GPIO.input(17)
    if status == 1:
        call ="on"
        message_button = "Turn Lights On"
        color = "error"
    elif status == 0:
        call = "off"
        message_button = "Turn Lights Off"
        color = "success"
    else:
        call = ""
        message_button = "Error"
        color = "error"
    print(status)
#            print(on_off)
    return  render_template('base.html',call=call,message_button=message_button,color=color)

@app.route('/lights/<on_off>', methods=['GET'])
def turn_lights(on_off: str = None):
    if on_off == "on":
        lights_on()
    elif on_off == "off":
        lights_off()
    else: 
        pass

    message_button = ""
    color = ""
    call = ""
    status = GPIO.input(17)
    if status == 1:
        call ="on"
        message_button = "Turn Lights On"
        color = "error"
    elif status == 0:
        call = "off"
        message_button = "Turn Lights Off"
        color = "success"
    else:
        call = ""
        message_button = "Error"
        color = "error"
    print(status)
    print(on_off)
    return  render_template('base.html',call=call,message_button=message_button,color=color)

@app.route('/water_plants',methods=['POST'])
def water_plants(ml = None):
    ml = request.form.get('ml')
    message = "Watering plant with "+str(ml)+"ml"
#   print(message)
#   water_plant(int(ml))
    message_button = ""
    color = ""
    call = ""
    status = GPIO.input(17)
#    status = 0
    if status == 1:
        call ="on"
        message_button = "Turn Lights On"
        color = "error"
    elif status == 0:
        call = "off"
        message_button = "Turn Lights Off"
        color = "success"
    else:
        call = ""
        message_button = "Error"
        color = "error"
    print(status)
#    print(on_off)
    print (message)
    print (type(float(ml)))
    start_thred = threading.Thread(target=water_plant,args=(float(ml),))
    start_thred.start()

    return render_template('water_plant.html',call=call,message_button=message_button,color=color,message=message)
@app.route('/logs')
def logs():
   file = "info.log"
   with open(file) as f:
       logs_content = f.readlines()
   logs_content = ''.join(logs_content)
   logs_content = logs_content.replace('\n','<br>')
   return render_template('logs.html',logs_content=logs_content)

#server = app.server()
   # return app
#app = create_app()
if __name__ == "__main__":
    app.run()
