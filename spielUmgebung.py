import random
import math
import numpy as np
import pygame

# Spielfeldgröße
fensterbreite = 400
fensterhohe = 400


# Farben
schwarz = (0, 0, 0)
weiß = (255, 255, 255)
gruen = (0, 255, 0)
rot = (255, 0, 0)

pygame.init()
display=pygame.display.set_mode((fensterbreite,fensterhohe))
clock=pygame.time.Clock()


def schlange(schlangen_position, anzeige):
    for position in schlangen_position:
        pygame.draw.rect(anzeige, gruen, pygame.Rect(position[0], position[1], 10, 10))


def apfel(apfel_position, anzeige):
    pygame.draw.rect(anzeige, rot, pygame.Rect(apfel_position[0], apfel_position[1], 10, 10))


def startposition():
    schlangen_start = [100, 100]
    schlangen_position = [[100, 100], [90, 100], [80, 100]]
    apfel_position = [random.randrange(1, 40) * 10, random.randrange(1, 40) * 10]
    punktestand = 0

    return schlangen_start, schlangen_position, apfel_position, punktestand


def apple_distance_from_snake(apple_position, snake_position):
    return np.linalg.norm(np.array(apple_position) - np.array(snake_position[0]))



def schlange_erzeugen(schlangen_start, schlangen_position, apfel_position, button_richtung, punktestand):
    if button_richtung == 1:
        schlangen_start[0] += 10
    elif button_richtung == 0:
        schlangen_start[0] -= 10
    elif button_richtung == 2:
        schlangen_start[1] += 10
    else:
        schlangen_start[1] -= 10

    if schlangen_start == apfel_position:
        apfel_position, punktestand = apple_collision(apfel_position, punktestand)
        schlangen_position.insert(0, list(schlangen_start))
    else:
        schlangen_position.insert(0, list(schlangen_start))
        schlangen_position.pop()

    return schlangen_position, apfel_position, punktestand


def apple_collision(apple_position, score):
    apple_position = [random.randrange(1, 40) * 10, random.randrange(1, 40) * 10]
    score += 1
    return apple_position, score


def boundaries_collision(snake_start):
    if snake_start[0] >= 400 or snake_start[0] < 0 or snake_start[1] >= 400 or snake_start[1] < 0:
        return 1
    else:
        return 0


def collision_with_self(snake_start, snake_position):
    # snake_start = snake_position[0]
    return 1 if snake_start in snake_position[1:] else 0


def is_direction_blocked(snake_position, current_direction_vector):
    next_step = snake_position[0] + current_direction_vector
    snake_start = snake_position[0]
    if boundaries_collision(next_step) == 1 or collision_with_self(next_step.tolist(), snake_position) == 1:
        return 1
    else:
        return 0


def blocked_directions(snake_position):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    is_front_blocked = is_direction_blocked(snake_position, current_direction_vector)
    is_left_blocked = is_direction_blocked(snake_position, left_direction_vector)
    is_right_blocked = is_direction_blocked(snake_position, right_direction_vector)

    return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked


def generate_random_direction(snake_position, angle_with_apple):
    direction = 0
    if angle_with_apple > 0:
        direction = 1
    elif angle_with_apple < 0:
        direction = -1
    else:
        direction = 0

    return direction_vector(snake_position, angle_with_apple, direction)


def direction_vector(snake_position, angle_with_apple, direction):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    new_direction = current_direction_vector

    if direction == -1:
        new_direction = left_direction_vector
    if direction == 1:
        new_direction = right_direction_vector

    button_direction = generate_button_direction(new_direction)

    return direction, button_direction


def play_game(snake_start, snake_position, apple_position, button_direction, score, display, clock, generation):
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        display.fill(schwarz)

        apfel(apple_position, display)
        schlange(snake_position, display)

        snake_position, apple_position, score = schlange_erzeugen(snake_start, snake_position, apple_position,
                                                               button_direction, score)
        pygame.display.set_caption(f"SCORE: {str(score)}; Generation: {str(generation)} ")
        pygame.display.update()
        clock.tick(5000)

        return snake_position, apple_position, score


def generate_button_direction(new_direction):
    button_direction = 0
    if new_direction.tolist() == [10, 0]:
        return 1
    elif new_direction.tolist() == [-10, 0]:
        return 0
    elif new_direction.tolist() == [0, 10]:
        return 2
    else:
        return 3

def angle_with_apple(snake_position, apple_position):
    apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
    snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
    norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
    if norm_of_apple_direction_vector == 0:
        norm_of_apple_direction_vector = 10
    if norm_of_snake_direction_vector == 0:
        norm_of_snake_direction_vector = 10

    apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
    snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
    angle = math.atan2(
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[1],
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[0]) / math.pi
    return angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized

