from collections import namedtuple
import numpy
import numpy.random
from numpy import array
from numpy.random import choice
import pygame
# import sys

# Logic Constants
# -----------------------------------------------------------------------------

# possible directions for the snake and their respective integer representation 
DIRECTIONS = {
      'W': 0,
      'N': 1,
      'E': 2,
      'S': 3
  }
# map DIRECTION to MOVEMENT vector that will be added to current head vector.
#  e.g. if head is located at (2, 1), i.e. 3rd column, 2nd row
#  and we get an input of 'N',
#  we add (0, -1) to the head location (vector addition).
#  of course this MOVEMENT vector is scaled by the size of the snake segment.
DIRECTIONS_TO_MOVEMENTS = {
      'W': (-1, 0),
      'N': (0, -1),
      'E': (1, 0),
      'S': (0, 1)
  }
SCREEN_TO_OBJECT_SCALE = 1/15  # 
Snake = namedtuple(
    'Snake',
    ['locations', 'direction']
)

# Display constants
# -------------------------------------------------------------------------------

BG_COLOR = ("#696969")
SNAKE_COLOR = ("#00bfff")
FRAMES_PER_SECOND = 16
SECONDS_PER_FRAME = 60 / FRAMES_PER_SECOND

# Logic functions
# -------------------------------------------------------------------------------


def get_fruit_dimensions(screen_dimensions,
                         scale=SCREEN_TO_OBJECT_SCALE):
    fruit_side = screen_dimensions[0] * scale
    return (fruit_side, fruit_side)


def get_segment_dimensions(screen_dimensions):
    ratio = 1
    width = screen_dimensions[0] * SCREEN_TO_OBJECT_SCALE
    length = width * ratio
    return (width, length)


def get_fruit(screen_dimensions, fruit=1) -> list:
    """
    return a list of random fruit locations

    :param screen_dimensions: int
    :param fruit: int

    :returns: list of numpy arrays
       each numpy array has 2 indexes defining the fruit location.
    """
    fruit_locations = [
        (choice(screen_dimensions[0]), choice(screen_dimensions[1]))
        for _ in range(fruit)
    ]
    return fruit_locations


def get_initial_snake(screen_dimensions):
    """
    Get the initial locations of snake and direction of the head.

    Coordinates origin is in top left corner of the screen.
    Segment position is given by the top left corner
    of the rectangle defining the segment,
    and it's horizontal and vertical dimensions.

    :param screen_dimensions: tuple
    x and y dimensions of screen.
    :returns: namedtuple (Snake)
    locations of snake segments and direction of snake head.
    """

    # get segment dimensions (horizontal, vertical)
    segment_dimensions = segment_width, segment_length= (
        get_segment_dimensions(screen_dimensions)
    )
    # head location top left corner (x, y, orientation)
    head = (
        screen_dimensions[0] - 2 * segment_width,
        screen_dimensions[1] // 2,
        0
    )

    head_x = head[0]
    head_y = head[1]
    tail = (
        head_x + segment_length,
        head_y,
        0
    )
    locations = [  # use numpy arrays to allow vector addition
        array(tail),
        array(head)
    ]
    direction = 'W'
    return Snake(locations, direction)


def initialize(screen_dimensions, n_fruit):
    return (
        get_initial_snake(screen_dimensions),
        get_fruit(screen_dimensions, n_fruit)
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


def get_next_snake(screen_dimensions: tuple, current_snake: Snake,
                   direction_from_input: str) -> Snake:
    segment_width, segment_length = get_segment_dimensions(screen_dimensions)
    current_locations = current_snake.locations
    # current_direction = current_snake.direction
    current_head_location = current_locations[-1][:2]
    # current_head_orientation = current_locations[-1][2]
    user_input = direction_from_input

    next_direction = get_next_direction(
        current_snake.direction,
        user_input
    )
    next_head_top_left = (
        current_head_location
        + array(DIRECTIONS_TO_MOVEMENTS[next_direction])
        * (segment_length / 2)
    )
    next_orientation = 0 if next_direction in ['E', 'W'] else 1
    next_head = numpy.append(
        next_head_top_left,
        next_orientation
    )
    next_locations = current_locations + [next_head]
    next_locations.pop(0)

    return Snake(
        locations=next_locations,
        direction=next_direction
    )


def elongate(screen_dimensions, snake, fruit):
    """check if snake hit a fruit, elongate snake and remove fruit.

    :param snake: Snake
    the current snake (locations and direction)
    :param fruit: list
    a list of fruit locations
    :returns: Snake
    current snake or an elongated snake if a fruit has been hit.
    """

    segment_width = get_segment_dimensions(screen_dimensions)[0]
    fruit_side = get_fruit_dimensions(screen_dimensions)[0]

    def is_head_fruit_overlap(head,
                              fruit_location):
        orientation = head[2]
        if orientation == 0:
            head_middle = (
                head[0],
                head[1] + segment_width / 2
            )
        else:
            head_middle = (
                head[0]
                + segment_width / 2, head[1]
            )

        is_middle_in_fruit_x = (
            fruit_location[0] < head_middle[0] < fruit_location[0] + fruit_side
        )
        is_middle_in_fruit_y = (
            fruit_location[1] < head_middle[1] < fruit_location[1] + fruit_side
        )
        if is_middle_in_fruit_x and is_middle_in_fruit_y:
            return True
        return False

    locations = snake.locations
    head = locations[-1]
    tail = locations[0]

    for i, fruit_location in enumerate(fruit):
        if is_head_fruit_overlap(head, fruit_location):
            new_tail = tail
            locations = [new_tail] + locations
            fruit.pop(i)

    return Snake(locations, snake.direction), fruit


def get_next_state(screen_dimensions, ):

    """
    Get next snake and fruit positions.

    Get next snake and then check if new snake head overlaps a fruit,
    and if so, elongate snake and remove the relevant fruit.

    :param screen_dimensions: tuple 

    :returns: tuple  (Snake object, list)
    The new Snake object and list of fruit locations.
    """

    pass


def game_over(screen_dimensions: tuple, snake: Snake) -> bool:
    """
    Check if game over conditions are met.

    :param screen_dimensions: tuple
    Screen width and height
    :param snake: Snake
    Snake locations and direction
    :returns: bool
    True if the game is over else False
    """
    body = snake.locations[:-1]
    head = snake.locations[-1]
    # check if head location overlaps any of the segments positions 
    for segment in body:
        if (array(head[:2]) == array(segment[:2])).all(): 
            return True
    # check if head x or y are larger than screen dimensions
    if head[0] > screen_dimensions[0] or head[1] > screen_dimensions[1]:
        return True
    # check if head x or y are smaller than zero
    if head[0] < 0 or head[1] < 0:
        return True
    return False


# Display functions
# -------------------------------------------------------------------------------


def get_segment_image(screen_dimensions, scale=1):
    """Create a snake segment image"""
    segment_width, segment_length = get_segment_dimensions(screen_dimensions)
    snake_surface = pygame.Surface((segment_width, segment_length))
    snake_surface.fill(SNAKE_COLOR)
    return snake_surface


def get_fruit_image(screen_dimensions,
                    path='skull-02.png'):
    """Load fruit image and process it for display."""
    fruit_dimensions = get_fruit_dimensions(screen_dimensions)
    image = pygame.image.load(path)
    image.convert()
    image = pygame.transform.scale(image, fruit_dimensions)
    return image


def main_loop(screen_dimensions=(640, 480), n_fruit=2):
    # initialize clock
    clock = pygame.time.Clock()

    # display setup
    pygame.display.set_caption("EGSAsnake")
    screen = pygame.display.set_mode(screen_dimensions)
    screen.fill(BG_COLOR)

    # get images for snake segment and fruit
    SEGMENT_IMAGE = get_segment_image(screen_dimensions)
    FRUIT_IMAGE = get_fruit_image(screen_dimensions)

    # initialize snake and fruit 
    snake, fruit = initialize(screen_dimensions, n_fruit)
    for location in snake.locations:
        screen.blit(SEGMENT_IMAGE, location[:2])
    for fruit_location in fruit:
        screen.blit(FRUIT_IMAGE, fruit_location)

    # setup for changing fruit locations on fixed time intervals
    frames_per_interval = 8
    timer_interval = int( 
        frames_per_interval
        * SECONDS_PER_FRAME
        * 100
    )
    fruit_timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(fruit_timer_event, timer_interval)
    new_fruit = False

    # infinite loop
    game_on = True
    while game_on:
        direction = snake.direction  # current head direction
        # loop through events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit if close button is pressed
                return
            if event.type == pygame.KEYDOWN: 
                key_pressed = event.key
                if key_pressed == pygame.K_q:  # quit if the 'q' key is pressed 
                    return
                # assign direction based on keyboard press
                else:
                    direction = ('W' if key_pressed == pygame.K_LEFT else
                                 'E' if key_pressed == pygame.K_RIGHT else
                                 'N' if key_pressed == pygame.K_UP else
                                 'S' if key_pressed == pygame.K_DOWN else
                                 None)
            # check fruit timer and set to True if timer elapsed
            if event.type == fruit_timer_event:
                new_fruit = True

        # get the next snake
        snake = get_next_snake(
            screen_dimensions,
            snake,
            direction
        )

        # get a new set of fruit if timer has elapsed
        fruit = get_fruit(screen_dimensions, n_fruit) if new_fruit else fruit
        new_fruit = False   # reset the new_fruit switch

        # elongate snake if any fruit has been eaten
        snake, fruit = elongate(screen_dimensions, snake, fruit)

        # clean the screen
        screen.fill(BG_COLOR)

        # check for game over
        if game_over(screen_dimensions, snake):
            snake, fruit = initialize(screen_dimensions, n_fruit)

        # blit new snake and fruit onto screen
        for location in snake.locations:
            screen.blit(SEGMENT_IMAGE, location[:2])
        for fruit_location in fruit:
            screen.blit(FRUIT_IMAGE, fruit_location)

        # redisplay the updated screen
        pygame.display.flip()

        # set the frames-per-second rate
        clock.tick(FRAMES_PER_SECOND)


if __name__ == "__main__":
    pygame.init()
    main_loop((640, 480), 3)
    pygame.quit()
    # sys.exit()
