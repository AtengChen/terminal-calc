from os import getppid, system
from sys import stderr, stdout
from text.text_style import *
import psutil
from keyboard import *
from termcolor import *
from text.text_color import *

parent_pid = getppid()
if psutil.Process(parent_pid).name() != 'cmd.exe':
    stderr.write('Couldn\'t found cmd.')
    exit()
else:
    _ = input('Press Enter to start...')

init()

mod = colored('''
 press %s %s %s %s to
  change buttons

press Enter to submit
press Ctrl+C to quit
''' % (up_tri, down_tri, left_tri, right_tri), color="yellow") + colored(b1+15*a1+b2+"\n"+b2, color="white", on_color="on_blue") + "%s" + colored("│\n├───────────────┤\n│", color="white", on_color="on_blue") + "%s" + colored("│\n├───┬───┬───┬───┤\n│ 7 │ 8 │ 9 │ / │\n├───┼───┼───┼───┤\n│ 4 │ 5 │ 6 │ * │\n├───┼───┼───┼───┤\n│ 1 │ 2 │ 3 │ - │\n├───┼───┼───┼───┤\n│ 0 │ ² │ √│ + │\n├───┴───│───┴───┤\n│       │       │\n│  CAL  │  CLS  │\n└───────┴───────┘", color="white", on_color="on_blue")

s = ''
x = 0
y = 2
l = '0'
c = [['7', '8', '9', '/'],
     ['4', '5', '6', '*'],
     ['1', '2', '3', '-'],
     ['0', '²', '√', '+'],
     ['cal', 'cal', 'cls', 'cls']]


def coord_converter(x, y, n):
    return {'x': len(c) - y, 'y': x}[n]


def update(string, letter):
    system('cls')
    init(autoreset=True)
    if len(string) > 7:
        string = 'OVERFLOW'
    if '√' not in string:
        string = 'formula:' + (7 - len(string)) * '_' + colored(string, color="red")
    else:
        string = 'formula:' + (6 - len(string)) * '_' + colored(string, color="red")
    if letter != '√':
        letter = 'current_num:' + (3 - len(letter)) * '_' + colored(letter, color="red")
    else:
        letter = 'current_num:' + (2 - len(letter)) * '_' + colored(letter, color="red")
    string = mod % (letter, string)
    stdout.write(string)


def parse(string):
    global s
    string = string.split('cal')[0]
    string = string.replace('²', '**2').replace('√', '**0.5')
    s = str(eval(string))
    s = str(round(float(s), 4))


def a(event):
    global s, x, y, l
    if event.event_type == 'down':
        if event.name == 'up':
            y += 1
        elif event.name == 'down':
            y -= 1
        elif event.name == 'left':
            x -= 1
        elif event.name == 'right':
            x += 1
        elif event.name == 'enter':
            if l == 'cls':
                s = ''
            elif l == 'cal':
                try:
                    parse(s)
                except:
                    s = 'ERROR'
            elif l == '√':
                update(s[:-1] + l + s[-1], l)
                s += l
                return
            else:
                s += l
        else:
            return
        _x = coord_converter(x, y, 'x') % 5
        _y = coord_converter(x, y, 'y') % 4
        l = c[_x][_y]
        update(s, l)


update(s, l)
hook(a)
while True:
    try:
        wait()
        _ = input()
    finally:
        exit()
