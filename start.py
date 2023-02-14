from HoverSerial import*
import threading
import time
import signal
from xbox360controller import Xbox360Controller

global_speed_left = 0
global_speed_right = 0
global_forward = True # 
SPEED_MAX_TEST = 300  # [-] Maximum speed for testing
SPEED_STEP = 2  # [-] Speed step
TIME_SEND = 0.1  # [s] Sending time interval


iStep = SPEED_STEP
iTest = 0
steer = 0
startTime = 0


def float_to_int(input_float):
    return int(input_float * 200)

def on_button_pressed(button):
    global global_forward
    global_forward = not global_forward

def on_trigger_moved(trigger):
    #print('Trigger {0} moved to {1}'.format(trigger.name, trigger.value))
    
    if(trigger.name == 'trigger_r'):
        global global_speed_right 
        global_speed_right = float_to_int(trigger.value)

    if(trigger.name == 'trigger_l'):
        global global_speed_left 
        global_speed_left = float_to_int(trigger.value)

def thread_receive_feedback():

    while True:

        feedback = hover_serial.receive_feedback()

        if feedback == None:
            print('No feedback')
            continue
        
        print('Receiving:\t', feedback)


if __name__ == "__main__":

    SERIAL_PORT = '/dev/serial0'
    SERIAL_BAUD = 115200
    hover_serial = Hoverboard_serial(SERIAL_PORT, SERIAL_BAUD)

    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            controller.trigger_r.when_moved = on_trigger_moved
            controller.trigger_l.when_moved = on_trigger_moved
            controller.button_a.when_pressed = on_button_pressed
            #global global_speed_right
            #global global_speed_left
            while True:
                
                # Send commands
                hover_serial.send_command(global_speed_left, global_speed_right)
                print('Sending:\t Speed Left: '+str(global_speed_left)+' Speed Right: '+str(global_speed_right))
                time.sleep(0.2)
            

            signal.pause()
    

    except KeyboardInterrupt:
        print("Keyboard interrupt...")

    except Exception as e:
        print("Error: " + str(e))

    finally:
        hover_serial.close()
