from collections import namedtuple
from numpy import array
from numpy.random import choice
import pygame
import sys
import numpy.random

numpy.random.choice

# possible directions for the snake and their respective integer representation 
DIRECTIONS = {
      'W': 0,
      'N': 1,
      'E': 2,
      'S': 3
  }
# map DIRECTION to MOVEMENT element that will be added to current head.
#  e.g. if head is located at (2, 1), i.e. 3rd row, 2nd column,
#  and we get an input of 'N',
#  we add (-1, 0) to the head location (vector addition)
DIRECTIONS_TO_MOVEMENTS = {
      'W': (-1, 0),
      'N': (0, -1),
      'E': (1, 0),
      'S': (0, 1)
  }

# # this is currently implemented using if else block
# #  using event.key as key to the map produces KeyError: 113
# KEYBOARD_TO_DIRECTIONS = {
#     pygame.K_LEFT: 'W',
#     pygame.K_RIGHT: 'E',
#     pygame.K_UP: 'N',
#     pygame.K_DOWN: 'S',
# }

TRANSFORM = 35

Snake = namedtuple(
    'Snake',
    ['locations', 'direction']
)

# Logic functions
# -------------------------------------------------------------------------------


def get_fruit(screen_size, fruit=1) -> list:
    """
    return a list of random fruit locations

    :param screen_size: int
    :param fruit: int

    :returns: list of numpy arrays
       each numpy array has 2 indexes defining the fruit location.
    """
    fruit_locations = [
        (choice(screen_size[0]), choice(screen_size[1]))
        for _ in range(fruit)
    ]
    return fruit_locations


def get_initial_snake(screen_size):
    '''
    get the initial locations of snake and direction of the head

    coordinates origin is in top left corner.
    '''
    # set the initial head location to middle of left side of the screen
    segment_length = screen_size[0] // TRANSFORM
    head = (screen_size[0] - segment_length, screen_size[1] // 2)
    head_x = head[0]
    head_y = head[1]

    locations = [  # use numpy arrays to allow vector addition
        array([head[0] + segment_length, head[1]]),
        array(head)
    ]
    direction = 'W'
    # InitialSnake = namedtuple(
    #     'Snake',
    #     ['locations', 'direction']
    # )
    return Snake(locations, direction)


def initialize(screen_size, n_fruit):
    return (
        get_initial_snake(screen_size),
        get_fruit(screen_size, n_fruit)
    )


def get_next_direction(current_direction,
                       direction_from_input) -> str:
    # if current direction is opposite to input direction
    #  or no input stay with current direction
    # otherwise return input direction
    next_direction = current_direction
    if direction_from_input:
        sum_directions = (
            DIRECTIONS[current_direction]
            + DIRECTIONS[direction_from_input]
        )
        if sum_directions % 2 != 0:
            next_direction = direction_from_input

    return next_direction


def get_next_snake(screen_size, current_snake,
                   direction_from_input) -> namedtuple:
    user_input = direction_from_input
    current_locations = current_snake.locations
    next_direction = get_next_direction(
        current_snake.direction,
        user_input
    )
    next_head = (
        current_locations[-1]
        + array(DIRECTIONS_TO_MOVEMENTS[next_direction])
        * (screen_size[0] / TRANSFORM)
    )
    next_locations = current_locations + [next_head]
    next_locations.pop(0)

    return Snake(
        locations=next_locations,
        direction=next_direction
    )


def elongate(snake, fruit):
    """check if snake hit a fruit, elongate snake and remove fruit.

    :param snake: Snake
    the current snake (locations and direction)
    :param fruit: list
    a list of fruit locations
    :returns: Snake
    current snake or an elongated snake if a fruit has been hit.
    """
    locations = snake.location
    head = locations[-1]
    tail = locations[0]
    for fruit_location in fruit:
        if head == fruit_location:
            # new_tail =
            # locations =
            pass
    pass


def game_over(screen_size: tuple, snake: Snake) -> bool:
    """Check if game over conditions are met.

    :param screen_size: tuple
    Screen width and height
    :param snake: namedtuple
    Snake locations and direction
    :returns:
    True if the game is over else False
    """
    body = snake.locations[:-1]
    head = snake.locations[-1]
    # check if head location overlaps any of the segments positions 
    for segment in body:
        if head == segment: 
            return True
    # check if head x or y are larger than screen dimensions
    if head[0] > screen_size[0] or head[1] > screen_size[1]:
        return True
    # check if head x or y are smaller than zero
    if head[0] < 0 or head[1] < 0:
        return True
    return False


# Display functions
# -------------------------------------------------------------------------------

BG_COLOR = ("#696969")
SNAKE_COLOR = ("#00bfff")




def get_segment(screen_size, scale=1):
    segment_width = screen_size[1] / TRANSFORM
    segment_length = screen_size[0] / TRANSFORM
    snake_surface = pygame.Surface((segment_width, segment_length))
    snake_surface.fill(SNAKE_COLOR)
    return snake_surface


# def transform
def main_loop(screen_size=(640, 480), n_fruit=2):

    # initialize clock
    clock = pygame.time.Clock()

    # display setup
    pygame.display.set_caption("EGSAsnake")
    screen = pygame.display.set_mode(screen_size)
    screen.fill(BG_COLOR)

    # rectangle image for snake segment
    SEGMENT_IMAGE = get_segment(screen_size)

    snake, fruit = initialize(screen_size, n_fruit)
    for location in snake.locations:
        screen.blit(SEGMENT_IMAGE, location)
    # print(f"initial snake:\n{snake}")
    game_on = True

    # setup for changing fruit location on fixed time intervals
    timer_interval = 10000 # 10.0 seconds
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, timer_interval)
    new_fruit = False
    while game_on:
        direction = snake.direction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
                if key_pressed == pygame.K_q:
                    return
                else:
                    direction = ('W' if key_pressed == pygame.K_LEFT else
                                 'E' if key_pressed == pygame.K_RIGHT else
                                 'N' if key_pressed == pygame.K_UP else
                                 'S' if key_pressed == pygame.K_DOWN else
                                 None)
            if event.type == timer_event:
                new_fruit = True
        snake = get_next_snake(
            screen_size,
            snake,
            direction
        )
        fruit = get_fruit(screen_size, n_fruit) if new_fruit else fruit
        new_fruit = False
        # print()
        # print(
        #     f"snake:\n{snake}"
        # )
        screen.fill(BG_COLOR)
        for location in snake.locations:
            screen.blit(SEGMENT_IMAGE, location)
        for fruit_location in fruit:
            screen.blit(SEGMENT_IMAGE, fruit_location)
        pygame.display.flip()
        clock.tick(10) # 2 frames per second


if __name__ == "__main__":
    pygame.init()
    main_loop((640, 480), 3)
    pygame.quit()
    sys.exit()
