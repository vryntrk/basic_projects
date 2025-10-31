import pygame
import random
import time

pygame.init()

width = 1024
height = 1024

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maganda Sim")
icon = pygame.image.load("game.png")
pygame.display.set_icon(icon)

background = pygame.transform.scale(pygame.image.load("road.png"), (width, height))

car_width = 100
car_height = 200
car_vel = 8
car = pygame.transform.scale(pygame.image.load("car.png"), (car_width, car_height))
car_coordinate = car.get_rect()
car_coordinate.x = (width - car_width) // 2
car_coordinate.y = height - car_height

enemy_width = 100
enemy_height = 200
enemy_vel = 5
enemy = pygame.transform.scale(pygame.image.load("enemy.png"), (enemy_width, enemy_height))
enemy_coordinate = enemy.get_rect()

broken_width = 100
broken_height = 200
broken_vel = 5
broken = pygame.transform.scale(pygame.image.load("broken.png"), (broken_width, broken_height))
broken_coordinate = broken.get_rect()

font = pygame.font.SysFont("comic sans", 32)

crash_sound = pygame.mixer.Sound("crash.mp3")
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1, 0.0)


def draw(enemies, brokens, elapsed_time):
    win.blit(background, (0, 0))

    win.blit(car, car_coordinate)

    for e in enemies:
        win.blit(enemy, e)

    for b in brokens:
        win.blit(broken, b)

    time_text = font.render(f"Time: {round(elapsed_time)}s", 1, "White")
    win.blit(time_text, (10, 10))

    pygame.display.update()


def columns():
    column_1 = 142
    column_2 = 330
    column_3 = 594
    column_4 = 782

    column_list = [column_1, column_2, column_3, column_4]

    selected_column = random.choice(column_list)
    return selected_column


def block():
    column_1 = 6
    column_2 = 462
    column_3 = 918

    column_list = [column_1, column_2, column_3]

    selected_column = random.choice(column_list)
    return selected_column



def main():
    run = True
    clock = pygame.time.Clock()

    enemy_count = 0
    enemy_add_increment = 3000
    enemies = []

    broken_count = 0
    broken_add_increment = 3500
    brokens = []

    start_time = time.time()

    hit = False

    while run:
        dt = clock.tick(120)
        enemy_count += dt
        broken_count += dt

        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_coordinate.left > 0:
            car_coordinate.x -= car_vel
        if keys[pygame.K_RIGHT] and car_coordinate.right < width:
            car_coordinate.x += car_vel

        if enemy_count > enemy_add_increment:
            for _ in range(2):
                enemy_coordinate.x = columns()
                enemy_rect = pygame.Rect(enemy_coordinate.x, -enemy_height, enemy_width, enemy_height)
                enemies.append(enemy_rect)
            enemy_count = 0
            enemy_add_increment = max(1500, enemy_add_increment-100)

        for e in enemies[:]:
            e.y += enemy_vel
            if e.y > height:
                enemies.remove(e)
            elif car_coordinate.colliderect(e):
                hit = True

        if broken_count > broken_add_increment:
            for _ in range(2):
                broken_coordinate.x = block()
                broken_rect = pygame.Rect(broken_coordinate.x, -broken_height, broken_width, broken_height)
                brokens.append(broken_rect)
            broken_count = 0
            broken_add_increment = max(2500, broken_add_increment-100)

        for b in brokens[:]:
            b.y += broken_vel
            if b.y > height:
                brokens.remove(b)
            elif car_coordinate.colliderect(b):
                hit = True

        if hit:
            pygame.mixer.music.stop()
            crash_sound.play()
            pygame.time.delay(150)
            game_over = font.render("Game Over!", 1, "White")
            win.blit(game_over, ((width - game_over.get_width())/2, (height - game_over.get_height())/2))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        draw(enemies, brokens, elapsed_time)

    pygame.quit()


main()
