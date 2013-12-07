__author__ = 'Helsloot'

WIDTH = 20
HEIGHT = 10
x = 0
y = 0
start_speed = 10

from ipy_lib import SnakeUserInterface

ui = SnakeUserInterface(WIDTH, HEIGHT, 1)
image = ui.WALL
ui.set_animation_speed(start_speed)


def processEvent(event):
    ui.print_(event.name + " " + event.data + "\n")
    if event.name == "alarm":
        processAnimation()
    if event.name == 'arrow':
        processArrow(event.data)
    if event.name == 'letter':
        processKey(event.data)


def processAnimation():
    global x, y
    if x < WIDTH:
        ui.place(x, y, image)
        ui.show()
        ui.place(x, y, ui.EMPTY)
        x += 1

    elif x == WIDTH:
        if y < HEIGHT - 1:
            x = 0
            y += 1
        else:
            x = 0
            y = 0


def processArrow(event_data):
    global start_speed
    if event_data == 'l':
        if start_speed > 0:
            start_speed -= 0.5
            ui.set_animation_speed(start_speed)

    elif event_data == 'r':
        start_speed += 0.5
        ui.set_animation_speed(start_speed)


def processKey(event_data):
    global image
    if event_data == 'g':
        if image == ui.SNAKE:
            image = ui.WALL
        else:
            image = ui.SNAKE


def count(n):
    for i in range(n*1000):
        i += 1
        print i
        if i == n*1000:
            print 'done!'

count(4)
# while True:
#     event = ui.get_event()
#     processEvent(event)
#

