from collections import namedtuple
import numpy as np
import pygame

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

def main_loop(screen_size=500):
    pygame.init()
    pygame.display.set_caption("Snakelan")

    screen = pygame.display.set_mode((screen_size, screen_size))
    clock = Clock()
    running = 1
    snake, fruit = intialize(screen_size, n_fruit)
    game_on = True
    while game_on:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
        user_input = # get input from pygame
        next_snake = get_next_snake(snake, user_input)
        fruit =
