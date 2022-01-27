import signal
from evdev import InputDevice, categorize, ecodes
from termcolor import cprint
import atexit

numericKeyPad = '/dev/input/event5'

def exit_handler():
    device.ungrab()

atexit.register(exit_handler)
 
device = InputDevice(numericKeyPad)

def handler(signum, frame):
    global device
    device.ungrab()
    exit(1)

# print(device)
device.grab()
 
signal.signal(signal.SIGINT, handler)


# print(device.capabilities(verbose=True))

# device.set_led(ecodes.LED_NUML, 0)
# print(device.leds(verbose=True))

def process(event):
    global n,list,flag
    key = ecodes.KEY[event.code][6:]
    if key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        n = n*10+int(ecodes.KEY[event.code][6:])
    if key in ['PLUS', 'MINUS', 'ENTER']:
        list.append(-1*n if flag else n)
        if n != 0:
            print()
        n = 0
        flag = True if key == 'MINUS' else False

    if key == 'ENTER':
        cprint('------------',color='yellow')
        cprint(f'{sum(list):>12}',color='blue',on_color='on_white')
        cprint('------------\n',color='yellow')
        
        list.clear()
        
    if flag:
        cprint(f'{n:>12}',end='\r',color='red')
    else:
        cprint(f'{n:>12}',end='\r',color='green')

    
        
n=0
list=[]
flag = False
cprint(f'{n:>12}',end='\r',color='green')
for event in device.read_loop():
    data = categorize(event)
    if event.type != ecodes.EV_KEY:
        continue
    elif data.keystate == 0: # ignore keyup
        continue
    process(event)
