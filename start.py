from HoverSerial import*
import threading
import time
import signal
from xbox360controller import Xbox360Controller

global_speed = 0
global_steer = 0
global_fast = False # 
SPEED_SLOW = 200  # [-] Maximum speed for testing
SPEED_HIGH = 500
TIME_SLEEP = 0.3  # [s] Sending time interval



def float_to_int(input_float):
    if(global_fast):
        return int(input_float * SPEED_HIGH)
    return int(input_float * SPEED_SLOW)

def on_button_pressed(button):
    global global_fast
    global_fast = not global_fast

def on_trigger_moved(trigger):
    #print('Trigger {0} moved to {1}'.format(trigger.name, trigger.value))    
    global global_speed 
    if(trigger.name == 'trigger_r'):
        #backwards
        global_speed = trigger.value * -1

    if(trigger.name == 'trigger_l'):
        #forward
        global_speed = trigger.value 
    
def on_axis_moved(axis):
    #print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    global global_steer
    if(abs(axis.x) < 0.5):
            global_steer =  0
    else:
        global_steer = axis.x

def convert_steering_and_speed_to_diff_drive(steering_value, speed_value):
    # Calculate the left and right wheel speeds
    if steering_value == 0:
        left_speed = speed_value
        right_speed = speed_value
    else:
        left_speed = (1 - abs(steering_value)) * (speed_value if steering_value > 0 else speed_value * (1 - abs(steering_value)))
        right_speed = (1 - abs(steering_value)) * (speed_value if steering_value < 0 else speed_value * (1 - abs(steering_value)))

    # Return the left and right wheel speeds
    return left_speed, right_speed


if __name__ == "__main__":

    SERIAL_PORT = '/dev/serial0'
    SERIAL_BAUD = 115200
    hover_serial = Hoverboard_serial(SERIAL_PORT, SERIAL_BAUD)

    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            controller.trigger_r.when_moved = on_trigger_moved
            controller.trigger_l.when_moved = on_trigger_moved
            controller.button_a.when_pressed = on_button_pressed
            controller.axis_l.when_moved = on_axis_moved
            while True:
                drive = convert_steering_and_speed_to_diff_drive(global_steer, global_speed)
                # Send commands
                hover_serial.send_command(float_to_int(drive[0]),float_to_int(drive[1]))
                #print('Sending Values left,rigt: ', float_to_int(drive[0]) ,float_to_int(drive[1]))
                print('Global values' ,global_speed, global_steer)
                time.sleep(0.3)

            

            signal.pause()
    

    except KeyboardInterrupt:
        print("Keyboard interrupt...")

    except Exception as e:
        print("Error: " + str(e))

    finally:
        hover_serial.close()
