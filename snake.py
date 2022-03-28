import numpy as np
from random import randint
from collections import namedtuple


# numbers representing snake and fruit on the screen matrix
# SNAKE = 1
FRUIT = -1

# possible directions for the snake
DIRECTIONS = ['W', 'N', 'E', 'S']
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


def get_fruit_locations(screen_size=20, fruit=1) -> list:
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


def get_initial_state(screen_size, snake_length):
    '''get the initial state of the screen, snake and fruit'''
    def get_initial_snake():
        '''get the initial locations of snake and direction of the head'''
        head = (screen_size // 2, screen_size-2)
        locations = [  # use numpy arrays to allow vector addition
            np.arrdkay(head[0], head[1]+1),
            np.array(head)
        ]
        direction = 'W'
        InitialSnake = namedtuple(
            'Snake',
            ['locations', 'direction']
        )
        return InitialSnake(locations, direction)

    # initialize screen, snake and fruit
    # screen = np.zeros(screen_size, screen_size)
    snake = get_initial_snake()
    fruit = get_fruit_location()  # default number of fruit is 1

    # # mark initial snake and fruit locations on screen
    # #  
    # i = 1
    # for location in snake.locations:
    #     screen[location] = i
    #     i += 1
    # for location in fruit.locations:
    #     screen[location] = FRUIT
    InitialState = namedtuple(
        'State', 
        ['snake', 'fruit']
    )
    return InitialState(snake=snake, fruit=fruit)


def get_next_fruit(screen_size) -> list:
    # retun a list of random fruit locations based on screen size, 
    return fruit


def get_next_direction(current_direction, user_input) -> str:
    # if direction opposite stay with same direction
    # if no input stay with same direction
    # otherwise return input
    return next_direction


def get_next_snake(current_state, get_input) -> namedtuple:
    user_input = get_input()
    current_locations = current_state.snake.locations
    next_direction = get_next_direction(
        current_state.snake.direction,
        user_input
    )
    next_head = (
        current_locations[-1]
        + MOVEMENTS[next_direction]
    )
    next_locations = current_locations + [next_head]
    Snake = namedtuple(
        'Snake',
        ['locations', 'direction']
    )
    return Snake(
        locations=next_locations,
        direction=next_direction
    )
    
