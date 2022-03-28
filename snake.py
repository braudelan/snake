import numpy as np
from random import randint
from collections import namedtuple


# numbers representing snake and fruit on the screen matrix
# SNAKE = 1
FRUIT = -1

# possible directions for the snake
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
MOVEMENTS = {
    'W': (0, -1),
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0)
}


def get_fruit(screen_size=20, fruit=1) -> list:
    """
    return a list of random fruit locations

    :param screen_size: int
    :param fruit: int

    :returns: list of numpy arrays
       each numpy array has 2 indexes defining the fruit location.
    """
    fruit_locations = [
        np.random.choice(screen_size, 2)  # 2 indexes randomly sampled from range(screen_size)
        for _ in range(fruit)
    ]
    return fruit_locations


# def get_initial_state(screen_size, snake_length):
#     '''get the initial state of the screen, snake and fruit'''

#     snake = get_initial_snake()
#     fruit = get_fruit_locations()  # default number of fruit is 1

#     InitialState = namedtuple(
#         'State', 
#         ['snake', 'fruit']
#     )
#     return InitialState(snake=snake, fruit=fruit)

def get_initial_snake(screen_size):
    '''get the initial locations of snake and direction of the head'''
    head = (screen_size // 2, screen_size-2)
    locations = [  # use numpy arrays to allow vector addition
        np.array([head[0], head[1] + 1]),
        np.array(head)
    ]
    direction = 'W'
    InitialSnake = namedtuple(
        'Snake',
        ['locations', 'direction']
    )
    return InitialSnake(locations, direction)


def get_next_direction(current_direction,
                       direction_from_input) -> str:
    # if current direction is opposite to input direction
    #  or no input stay with current direction
    # otherwise return input direction
    sum_directions = (
        DIRECTIONS[current_direction]
        + DIRECTIONS[direction_from_input]
    )
    if direction_from_input and sum_directions % 2 != 0:
        next_direction = direction_from_input
    else:
        next_direction = current_direction
    return next_direction


def get_next_snake(current_snake,
                   direction_from_input) -> namedtuple:
    user_input = direction_from_input
    current_locations = current_snake.locations
    next_direction = get_next_direction(
        current_snake.direction,
        user_input
    )
    next_head = (
        current_locations[-1]
        + MOVEMENTS[next_direction]
    )
    next_locations = current_locations + [next_head]
    next_locations.pop(0)
    Snake = namedtuple(
        'Snake',
        ['locations', 'direction']
    )
    return Snake(
        locations=next_locations,
        direction=next_direction
    )


