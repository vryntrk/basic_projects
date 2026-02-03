import pygame
import random
import time
import ctypes
import platform

if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass

pygame.init()

width = 800
height = 800

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maganda Sim")
icon = pygame.image.load("pictures/logo.png")
pygame.display.set_icon(icon)

background = pygame.transform.scale(pygame.image.load("pictures/road.png"), (width, height))

car_width = 80
car_height = 160
car = pygame.transform.scale(pygame.image.load("pictures/car.png"), (car_width, car_height))
car_coordinate = car.get_rect()
car_coordinate.x = (width - car_width) // 2
car_coordinate.y = height - car_height
car_mask = pygame.mask.from_surface(car)

enemy_width = 80
enemy_height = 160
enemy = pygame.transform.scale(pygame.image.load("pictures/enemy.png"), (enemy_width, enemy_height))
enemy_coordinate = enemy.get_rect()
enemy_mask = pygame.mask.from_surface(enemy)

broken_width = 80
broken_height = 160
broken = pygame.transform.scale(pygame.image.load("pictures/broken.png"), (broken_width, broken_height))
broken_coordinate = broken.get_rect()
broken_mask = pygame.mask.from_surface(broken)

font = pygame.font.SysFont("comic sans", 32)

crash_sound = pygame.mixer.Sound("sounds/crash.mp3")
pygame.mixer.music.load("sounds/background.mp3")
pygame.mixer.music.play(-1, 0.0)


def draw(bg_y, enemies, broken_ones, elapsed_time, speed):
    win.blit(background, (0, bg_y))
    win.blit(background, (0, bg_y - height))

    win.blit(car, car_coordinate)

    for e in enemies:
        win.blit(enemy, e)

    for b in broken_ones:
        win.blit(broken, b)

    time_text = font.render(f"Time: {round(elapsed_time)}s", 1, "White", "Black")
    win.blit(time_text, (10, 10))

    speedometer = font.render(f"Speed: {speed}", 1, "White", "Black")
    win.blit(speedometer, ((790 - speedometer.get_width()), 10))


def columns():
    column_1 = 100
    column_2 = 260
    column_3 = 450
    column_4 = 610

    column_list = [column_1, column_2, column_3, column_4]

    selected_column = random.choice(column_list)
    return selected_column


def block():
    column_1 = 0
    column_2 = 360
    column_3 = 720

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
    broken_ones = []

    start_time = time.time()

    background_y = 0
    background_speed = 5
    car_vel = 5
    broken_vel = 8
    enemy_vel = 5

    slow_motion = False
    slow_motion_timer = 0

    hit = False

    while run:
        dt = clock.tick(120)
        enemy_count += dt
        broken_count += dt
        background_y += background_speed

        if background_y >= height:
            background_y = 0

        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if background_speed < 10:
                        background_speed += 1
                        broken_vel += 1
                        enemy_vel += 1
                if event.key == pygame.K_DOWN:
                    if background_speed > 5:
                        background_speed -= 1
                        broken_vel -= 1
                        enemy_vel -= 1
                    elif background_speed <= 5:
                        slow_motion = True
                        background_speed, broken_vel, enemy_vel, car_vel = 2, 2, 2, 2

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
            offset = (e.x - car_coordinate.x, e.y - car_coordinate.y)
            if e.y > height:
                enemies.remove(e)
            elif car_mask.overlap(enemy_mask, offset):
                hit = True

        if broken_count > broken_add_increment:
            for _ in range(2):
                broken_coordinate.x = block()
                broken_rect = pygame.Rect(broken_coordinate.x, -broken_height, broken_width, broken_height)
                broken_ones.append(broken_rect)
            broken_count = 0
            broken_add_increment = max(2500, broken_add_increment-100)

        for b in broken_ones[:]:
            b.y += broken_vel
            offset = (b.x - car_coordinate.x, b.y - car_coordinate.y)
            if b.y > height:
                broken_ones.remove(b)
            elif car_mask.overlap(broken_mask, offset):
                hit = True

        if hit:
            pygame.mixer.music.stop()
            crash_sound.play()
            pygame.time.delay(150)
            game_over = font.render("Game Over!", 1, "White")
            win.blit(game_over, ((width - game_over.get_width()) // 2, (height - game_over.get_height()) // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        if slow_motion:
            slow_motion_timer += dt
            if slow_motion_timer >= 3000:
                slow_motion = False
                background_speed = 5
                broken_vel = 8
                enemy_vel = 5
                car_vel = 5
                slow_motion_timer = 0

        draw(background_y, enemies, broken_ones, elapsed_time, background_speed)

        if slow_motion:
            blue_filter = pygame.Surface((width, height))
            blue_filter.fill((48, 213, 200))
            blue_filter.set_alpha(100)
            win.blit(blue_filter, (0, 0))
        pygame.display.update()

    pygame.quit()


main()
