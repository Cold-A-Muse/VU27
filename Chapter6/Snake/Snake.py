'''
Assignment: Snake
Created on 8th of december 2013
Author: Daan Helsloot (dht340)
'''

WIDTH = 30
HEIGHT = 40

from Coordinate import Coordinate
from SnakeCoordinateRow import SnakeCoordinateRow
from ipy_lib import SnakeUserInterface

start_speed = 5
apple_x = 0
apple_y = 0
current_direction = 'r'
ui = SnakeUserInterface(WIDTH, HEIGHT)
ui.set_animation_speed(start_speed)
snake_instance = SnakeCoordinateRow()


def process_event(event):
    if event.name == "alarm":
        chk_snake_tail_collision(snake_instance)
        process_animation()
    if event.name == 'arrow':
        set_direction(event.data)


def create_snake():
    global snake_instance
    snake_instance.add(Coordinate(0, 0))
    snake_instance.add(Coordinate(1, 0))


def put_snake_on_board(snake_instance):
    for snake_coordinate in snake_instance.snake_tail:
        ui.place(snake_coordinate.x, snake_coordinate.y, ui.SNAKE)
    ui.show()


def set_up_game():
    create_snake()
    set_apple_image()
    put_snake_on_board(snake_instance)


def set_apple_image():
    global apple_x, apple_y
    apple_x = ui.random(WIDTH - 1)
    apple_y = ui.random(HEIGHT - 1)
    ui.place(apple_x, apple_y, ui.FOOD)
    ui.show()


def chk_snake_tail_collision(snake_instance):
    for i in range(0, len(snake_instance.snake_tail)-1):
        if snake_instance.snake_tail[-1].x == snake_instance.snake_tail[i].x and \
           snake_instance.snake_tail[-1].y == snake_instance.snake_tail[i].y:
            ui.print_("You're dead!")
            ui.set_animation_speed(0)


def chk_apple_caught():
    global apple_x, apple_y
    if snake_instance.snake_tail[-1].x == apple_x and snake_instance.snake_tail[-1].y == apple_y:
        snake_instance.add(Coordinate(apple_x, apple_y))
        ui.place(apple_x, apple_y, ui.SNAKE)
        ui.show()
        for i in range(0, len(snake_instance.snake_tail)-1):
            while snake_instance.snake_tail[i].x == apple_x and snake_instance.snake_tail[i].y == apple_y:
                apple_x = ui.random(WIDTH - 1)
                apple_y = ui.random(HEIGHT - 1)
    ui.place(apple_x, apple_y, ui.FOOD)
    ui.show()


def set_direction(event_data):
    global current_direction
    if event_data == 'r' and current_direction != 'l':
        current_direction = 'r'
    elif event_data == 'l' and current_direction != 'r':
        current_direction = 'l'
    elif event_data == 'u' and current_direction != 'd':
        current_direction = 'u'
    elif event_data == 'd' and current_direction != 'u':
        current_direction = 'd'


def check_boundary_collision(coordinate):
    if coordinate.x == WIDTH:
        coordinate.x = 0
    if coordinate.x < 0:
        coordinate.x = WIDTH - 1
    if coordinate.y == HEIGHT:
        coordinate.y = 0
    if coordinate.y < 0:
        coordinate.y = HEIGHT - 1


def process_animation():
    global apple_x, apple_y
    x = snake_instance.snake_tail[-1].x
    y = snake_instance.snake_tail[-1].y
    if apple_x == x and apple_y == y:
        set_apple_image()
    else:
        old_coord = snake_instance.remove()
        ui.place(old_coord.x, old_coord.y, ui.EMPTY)

    if current_direction == 'r':
        x += 1
        new_coord = Coordinate(x, y)
        check_boundary_collision(new_coord)
        snake_instance.add(new_coord)

    elif current_direction == 'l':
        x -= 1
        new_coord = Coordinate(x, y)
        check_boundary_collision(new_coord)
        snake_instance.add(new_coord)

    elif current_direction == 'u':
        y -= 1
        new_coord = Coordinate(x, y)
        check_boundary_collision(new_coord)
        snake_instance.add(new_coord)

    elif current_direction == 'd':
        y += 1
        new_coord = Coordinate(x, y)
        check_boundary_collision(new_coord)
        snake_instance.add(new_coord)

    ui.place(new_coord.x, new_coord.y, ui.SNAKE)
    ui.show()


set_up_game()

while True:
    event = ui.get_event()
    process_event(event)

