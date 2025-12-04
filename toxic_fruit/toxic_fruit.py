import pygame
import time
import random

pygame.init()
font = pygame.font.SysFont('elephant', 30)

width = 1024
height = 1024
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Toxic Fruit')

icon = pygame.image.load('pictures/game.png')
pygame.display.set_icon(icon)

background = pygame.transform.scale(pygame.image.load("pictures/background.png"), (width, height))

apple_width = 75
apple_height = 75
apple = pygame.transform.scale(pygame.image.load("pictures/apple.png"), (apple_width, apple_height))

pear_width = 75
pear_height = 75
pear = pygame.transform.scale(pygame.image.load("pictures/pear.png"), (pear_width, pear_height))

banana_width = 75
banana_height = 75
banana = pygame.transform.scale(pygame.image.load("pictures/banana.png"), (banana_width, banana_height))

antidote_width = 75
antidote_height = 75
antidote = pygame.transform.scale(pygame.image.load("pictures/antidote.png"), (antidote_width, antidote_height))

eat_sound = pygame.mixer.Sound('sounds/eat.mp3')
heal_sound = pygame.mixer.Sound('sounds/heal.mp3')


def poisonous_fruit(apple_c, pear_c, banana_c):
    options = []
    if apple_c > 0:
        options.append('apple')
    if pear_c > 0:
        options.append('pear')
    if banana_c > 0:
        options.append('banana')
    options.append(None)
    return random.choice(options)


def fruit_object(picture, number):
    text = font.render(str(number), True, (255, 255, 255))

    WIDTH = picture.get_width() + 10 + text.get_width()
    HEIGHT = max(picture.get_height(), text.get_height())

    sticker = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    sticker.blit(picture, (0, 0))

    text_y = (HEIGHT - text.get_height()) // 2
    sticker.blit(text, (picture.get_width() + 10, text_y))

    return sticker



def draw(apple_count, pear_count, banana_count, antidote_count, countdown):
    win.blit(background, (0, 0))

    pygame.draw.line(win, (255, 255, 255), (0, 99), (width, 99), 1)
    pygame.draw.line(win, (255, 255, 255), (width // 4 - 1, 0), (width // 4 - 1, 100), 1)
    pygame.draw.line(win, (255, 255, 255), (2 * width // 4 - 1, 0), (2 * width // 4 - 1, 100), 1)
    pygame.draw.line(win, (255, 255, 255), (3 * width // 4 - 1, 0), (3 * width // 4 - 1, 100), 1)

    apple_object = fruit_object(apple, apple_count)
    apple_x = (width // 4 - apple_object.get_width()) // 2
    apple_y = (100 - apple_object.get_height()) // 2
    win.blit(apple_object, (apple_x, apple_y))

    pear_object = fruit_object(pear, pear_count)
    pear_x = (width // 4 - pear_object.get_width()) // 2 + width // 4
    pear_y = (100 - pear_object.get_height()) // 2
    win.blit(pear_object, (pear_x, pear_y))

    banana_object = fruit_object(banana, banana_count)
    banana_x = (width // 4 - banana_object.get_width()) // 2 + width // 2
    banana_y = (100 - banana_object.get_height()) // 2
    win.blit(banana_object, (banana_x, banana_y))

    antidote_object = fruit_object(antidote, antidote_count)
    antidote_x = (width // 4 - antidote_object.get_width()) // 2 + 3 * width // 4
    antidote_y = (100 - antidote_object.get_height()) // 2
    win.blit(antidote_object, (antidote_x, antidote_y))

    time_text = font.render(f"Time: {round(countdown, 1)} s", True, (255, 255, 255), (0, 0, 0 ))
    win.blit(time_text, ((width - time_text.get_width()) // 2, 100))


def win_message():
    message = font.render("Congrats, you ate all the fruits successfully!", True, (255, 255, 255), (0, 0, 0 ))
    win.blit(message, ((width - message.get_width()) // 2, (height - message.get_height()) // 2))
    pygame.display.update()


def death_message():
    message = font.render("You failed, you died!", True, (255, 255, 255), (0, 0, 0 ))
    win.blit(message, ((width - message.get_width()) // 2, (height - message.get_height()) // 2))
    pygame.display.update()


def colorful_filter():
    red_filter = pygame.Surface((width, height))
    red_filter.fill((255, 0, 0))
    red_filter.set_alpha(128)

    green_filter = pygame.Surface((width, height))
    green_filter.fill((0, 255, 0))
    green_filter.set_alpha(128)

    black_filter = pygame.Surface((width, height))
    black_filter.fill((0, 0, 0))
    black_filter.set_alpha(200)

    filters = [red_filter, green_filter, black_filter]
    return filters


def main():
    run = True

    clock = pygame.time.Clock()
    start_time = time.time()
    total_time = 5

    apple_count = 5
    pear_count = 5
    banana_count = 5
    antidote_count = 3

    current_poison = poisonous_fruit(apple_count, pear_count, banana_count)

    is_poisoned = False
    screen_filter = colorful_filter()

    while run:
        clock.tick(60)

        current_time = time.time()
        elapsed_time = current_time - start_time
        countdown = total_time - elapsed_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    if current_poison == "apple":
                        is_poisoned = True
                        start_time = time.time() - 4
                    elif apple_count > 0 and not is_poisoned:
                        eat_sound.play()
                        apple_count -= 1
                        start_time = time.time()
                    current_poison = poisonous_fruit(apple_count, pear_count, banana_count)

                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    if current_poison == "pear":
                        is_poisoned = True
                        start_time = time.time() - 4
                    elif pear_count > 0 and not is_poisoned:
                        eat_sound.play()
                        pear_count -= 1
                        start_time = time.time()
                    current_poison = poisonous_fruit(apple_count, pear_count, banana_count)

                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    if current_poison == "banana":
                        is_poisoned = True
                        start_time = time.time() - 4
                    elif banana_count > 0 and not is_poisoned:
                        eat_sound.play()
                        banana_count -= 1
                        start_time = time.time()
                    current_poison = poisonous_fruit(apple_count, pear_count, banana_count)

                elif (event.key == pygame.K_4 or event.key == pygame.K_KP4) and is_poisoned:
                    if antidote_count > 0:
                        heal_sound.play()
                        antidote_count -= 1
                        is_poisoned = False
                        win.blit(screen_filter[1], (0, 0))
                        pygame.display.update()
                        pygame.time.delay(100)
                        start_time = time.time()
                    current_poison = poisonous_fruit(apple_count, pear_count, banana_count)

        draw(apple_count, pear_count, banana_count, antidote_count, countdown)

        if is_poisoned:
            win.blit(screen_filter[2], (0, 0))

        pygame.display.update()

        if apple_count == 0 and pear_count == 0 and banana_count == 0 and antidote_count >= 0:
            win_message()
            pygame.time.delay(3000)
            run = False
        if countdown <= 0:
            win.blit(screen_filter[0], (0, 0))
            death_message()
            pygame.time.delay(3000)
            run = False

    pygame.quit()


main()
