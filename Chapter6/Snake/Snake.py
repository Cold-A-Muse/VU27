__author__ = 'Helsloot'

from Coordinate import Coordinate
from SnakeCoordinateRow import SnakeCoordinateRow
from ipy_lib import SnakeUserInterface

WIDTH = 10
HEIGHT = 10
start_speed = 5

apple_x = 0
apple_y = 0
current_direction = 'r'
dead = False
ui = SnakeUserInterface(WIDTH, HEIGHT)
image = ui.WALL
ui.set_animation_speed(start_speed)
head_coordinate = Coordinate(1, 0)
snake_instance = SnakeCoordinateRow()


def processEvent(event):
    if event.name == "alarm":
        processAnimation()
    if event.name == 'arrow':
        set_current_direction(event.data)
    # if event.name == 'letter':
    #     processKey(event.data)


def create_snake():
    global snake_instance
    snake_instance.add(Coordinate(1, 0))


# def put_snake_on_board(snake_instance):
#     for snake_coordinate in snake_instance.snake_tail:
#         ui.place(snake_coordinate.x, snake_coordinate.y, ui.SNAKE)
#     ui.show()

def put_snake_on_board():
    ui.place(head_coordinate.x, head_coordinate.y, ui.SNAKE)
    ui.show()

def set_apple_image_solo():
    global apple_x, apple_y
    apple_x = ui.random(WIDTH - 1)
    apple_y = ui.random(HEIGHT - 1)
    ui.place(apple_x, apple_y, ui.FOOD)
    ui.show()


def chk_apple_caught():
    global head_coordinate, apple_x, apple_y
    if head_coordinate.x == apple_x and head_coordinate.y == apple_y:
        ui.place(apple_x, apple_y, ui.SNAKE)
        apple_x = ui.random(WIDTH - 1)
        apple_y = ui.random(HEIGHT - 1)
    ui.place(apple_x, apple_y, ui.FOOD)
    ui.show()


def set_current_direction(event_data):
    global current_direction
    if event_data == 'r':
        current_direction = 'r'
    elif event_data == 'l':
        current_direction = 'l'
    elif event_data == 'u':
        current_direction = 'u'
    elif event_data == 'd':
        current_direction = 'd'


def processAnimation():
    global head_coordinate, current_direction, dead, ui
    ui.place(head_coordinate.x, head_coordinate.y, ui.EMPTY)
    if current_direction == 'r':
        if head_coordinate.x < WIDTH - 1:
            head_coordinate.shift(1, 0)
            ui.place(head_coordinate.x, head_coordinate.y, ui.SNAKE)
            ui.show()
        else:
            dead = True
    elif current_direction == 'l':
        if head_coordinate.x > 0:
            head_coordinate.shift(-1, 0)
            ui.place(head_coordinate.x, head_coordinate.y, ui.SNAKE)
            ui.show()
        else:
            dead = True
    elif current_direction == 'u':
        if head_coordinate.y > 0:
            head_coordinate.shift(0, -1)
            ui.place(head_coordinate.x, head_coordinate.y, ui.SNAKE)
            ui.show()
        else:
            dead = True
    elif current_direction == 'd':
        if head_coordinate.y < HEIGHT - 1:
            head_coordinate.shift(0, 1)
            ui.place(head_coordinate.x, head_coordinate.y, ui.SNAKE)
            ui.show()
        else:
            dead = True


def check_dead_state():
    global dead
    if dead:
        ui.clear_text()
        ui.print_("You're dead")
        ui.clear()
        ui.show()


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


create_snake()
set_apple_image_solo()
put_snake_on_board()

while True:
    event = ui.get_event()
    processEvent(event)
    check_dead_state()
    chk_apple_caught()


