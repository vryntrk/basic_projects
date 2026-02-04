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
pygame.display.set_caption("Eater")
icon = pygame.image.load("pictures/logo.png")
pygame.display.set_icon(icon)

background = pygame.transform.scale(pygame.image.load("pictures/sea.png"), (width, height))

hunter_width = 100
hunter_height = 50
hunter_vel = 4
hunter_img = pygame.image.load("pictures/shark.png")
hunter = pygame.transform.scale(hunter_img, (hunter_width, hunter_height))
hunter_coordinate = hunter.get_rect()
hunter_coordinate.x = (width - hunter_width) // 2
hunter_coordinate.y = (height - hunter_height) // 2
hunter_mask = pygame.mask.from_surface(hunter)

food_width = 60
food_height = 30
food_img = pygame.image.load("pictures/salmon.png")
food = pygame.transform.scale(food_img, (food_width, food_height))
food_coordinate = food.get_rect()
food_mask = pygame.mask.from_surface(food)

bomb_width = 50
bomb_height = 50
bomb_img = pygame.image.load("pictures/bomb.png")
bomb = pygame.transform.scale(bomb_img, (bomb_width, bomb_height))
bomb_coordinate = bomb.get_rect()
bomb_mask = pygame.mask.from_surface(bomb)

heal_width = 50
heal_height = 50
heal_img = pygame.image.load("pictures/heart.png")
heal = pygame.transform.scale(heal_img, (heal_width, heal_height))
heal_coordinate = heal.get_rect()
heal_mask = pygame.mask.from_surface(heal)

font = pygame.font.SysFont("consolas", 32)

eat_sound = pygame.mixer.Sound("sounds/eat.mp3")
damage_sound = pygame.mixer.Sound("sounds/explosion.mp3")
upgrade_sound = pygame.mixer.Sound("sounds/upgrade.mp3")
heal_sound = pygame.mixer.Sound("sounds/heal.mp3")
pygame.mixer.music.load("sounds/background.mp3")


def music_on():
    music_on_text = font.render("Music On -M-", 1, "White")
    win.blit(music_on_text, ((width - music_on_text.get_width()) // 2, (95 - music_on_text.get_height()) // 2))


def music_off():
    music_off_text = font.render("Music Off -M-", 1, "White")
    win.blit(music_off_text, ((width - music_off_text.get_width()) // 2, (95 - music_off_text.get_height()) // 2))


def draw(hunter_image, hunter_rect, foods, bombs, score_point, hearts, heal_list, music):
    win.blit(background, (0, 0))
    pygame.draw.line(win, "white", (0, 95), (width, 95), 5)

    win.blit(hunter_image, hunter_rect)

    for f in foods:
        win.blit(food, f[0])

    for b in bombs:
        win.blit(bomb, b[0])

    for h in heal_list:
        win.blit(heal, h[0])

    score_text = font.render(f"Score: {score_point}", 1, "White")
    win.blit(score_text, (50, (95 - score_text.get_height()) // 2))

    remaining_hearts = font.render(f"Hearts: {hearts}", 1, "White")
    win.blit(remaining_hearts, (width - remaining_hearts.get_width() - 50, (95 - score_text.get_height()) // 2))

    if music:
        music_on()
    else:
        music_off()


def the_end(score_point):
    message_1 = font.render(f"Game Over! Your Score: {score_point}", 1, "White")
    win.blit(message_1, ((width - message_1.get_width()) // 2, height // 2 - message_1.get_height() - 20))
    message_2 = font.render("Press 'R' to restart or 'ESC' to quit.", 1, "White")
    win.blit(message_2, ((width - message_2.get_width()) // 2, height // 2 - message_2.get_height() + 20))
    pygame.display.update()


def main():
    global hunter, hunter_coordinate, hunter_width, hunter_height, hunter_vel
    angle = 0
    hunter_right = hunter
    hunter_left = pygame.transform.flip(hunter, True, False)
    growth_point = 750

    run = True
    clock = pygame.time.Clock()

    food_count = 0
    food_add_increment = 2000
    foods = []

    bomb_count = 0
    bomb_add_increment = 4000
    bombs = []

    hearts = 3

    heal_count = 0
    heal_add_increment = 1000
    heal_list = []

    score_point = 0

    hit = False

    music = True
    if music:
        pygame.mixer.music.play(-1, 0.0)

    while run:
        dt = clock.tick(120)
        food_count += dt
        bomb_count += dt
        heal_count += dt

        elapsed_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    music = not music
                    if music:
                        pygame.mixer.music.play(-1, 0.0)
                    else:
                        pygame.mixer.music.stop()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if keys[pygame.K_LEFT]:
                angle = 135
            elif keys[pygame.K_RIGHT]:
                angle = 45
            else:
                angle = 90
        elif keys[pygame.K_DOWN]:
            if keys[pygame.K_LEFT]:
                angle = 225
            elif keys[pygame.K_RIGHT]:
                angle = 315
            else:
                angle = 270
        elif keys[pygame.K_LEFT]:
            angle = 180
        elif keys[pygame.K_RIGHT]:
            angle = 0

        if 90 < angle < 270:
            base_img = hunter_left
            current_angle = angle - 180
        else:
            base_img = hunter_right
            current_angle = angle

        rotated_hunter = pygame.transform.rotate(base_img, current_angle)
        new_rect = rotated_hunter.get_rect(center=(hunter_coordinate.centerx, hunter_coordinate.centery))
        current_hunter_mask = pygame.mask.from_surface(rotated_hunter)

        if keys[pygame.K_LEFT] and hunter_coordinate.x > 0:
            hunter_coordinate.x -= hunter_vel
        if keys[pygame.K_RIGHT] and hunter_coordinate.x < width - hunter_width:
            hunter_coordinate.x += hunter_vel
        if keys[pygame.K_UP] and hunter_coordinate.y > 100:
            hunter_coordinate.y -= hunter_vel
        if keys[pygame.K_DOWN] and hunter_coordinate.y < height - hunter_height:
            hunter_coordinate.y += hunter_vel

        if food_count > food_add_increment:
            for _ in range(3):
                food_coordinate.x = random.randint(0, width - food_width)
                food_coordinate.y = random.randint(100, height - food_height)
                food_rect = pygame.Rect(food_coordinate.x, food_coordinate.y, food_width, food_height)
                new_food = [food_rect, time.time()]
                foods.append(new_food)
            food_count = 0
            food_add_increment = 2000

        for f in foods[:]:
            offset = (f[0].x - new_rect.x, f[0].y - new_rect.y)
            if current_hunter_mask.overlap(food_mask, offset):
                eat_sound.play()
                foods.remove(f)
                score_point += 50
            else:
                if elapsed_time - f[1] > 5:
                    foods.remove(f)

        if score_point == growth_point:
            upgrade_sound.play()

            hunter_width += 20
            hunter_height += 10

            hunter_img_scaled = pygame.transform.scale(hunter_img, (hunter_width, hunter_height))
            hunter_right = hunter_img_scaled
            hunter_left = pygame.transform.flip(hunter_right, True, False)

            previous_center = hunter_coordinate.center
            hunter_coordinate = hunter_right.get_rect()
            hunter_coordinate.center = previous_center

            growth_point += 750
            hunter_vel -= 0.1

        if bomb_count > bomb_add_increment:
            for _ in range(2):
                bomb_coordinate.x = random.randint(0, width - bomb_width)
                bomb_coordinate.y = random.randint(100, height - bomb_height)
                bomb_rect = pygame.Rect(bomb_coordinate.x, bomb_coordinate.y, bomb_width, bomb_height)
                new_bomb = [bomb_rect, time.time()]
                bombs.append(new_bomb)
            bomb_count = 0
            bomb_add_increment = max(2500, bomb_add_increment - 500)

        for b in bombs[:]:
            offset = (b[0].x - new_rect.x, b[0].y - new_rect.y)
            if current_hunter_mask.overlap(bomb_mask, offset):
                bombs.remove(b)
                hearts -= 1
                damage_sound.play()
            else:
                if elapsed_time - b[1] > 5:
                    bombs.remove(b)

        if hearts < 3 and heal_count > heal_add_increment:
            for _ in range(1):
                heal_coordinate.x = random.randint(0, width - heal_width)
                heal_coordinate.y = random.randint(100, height - heal_height)
                heal_rect = pygame.Rect(heal_coordinate.x, heal_coordinate.y, heal_width, heal_height)
                new_heal = [heal_rect, time.time()]
                heal_list.append(new_heal)
            heal_count = 0
            heal_add_increment = max(3500, heal_add_increment + 500)

        for h in heal_list[:]:
            offset = (h[0].x - new_rect.x, h[0].y - new_rect.y)
            if current_hunter_mask.overlap(heal_mask, offset):
                heal_list.remove(h)
                hearts += 1
                heal_sound.play()
            else:
                if elapsed_time - h[1] > 5 or hearts == 3:
                    heal_list.remove(h)

        if hearts == 0:
            hit = True

        if hit:
            pygame.mixer.music.stop()
            pygame.time.delay(150)
            the_end(score_point)
            pygame.time.delay(3000)

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return True
                        if event.key == pygame.K_ESCAPE:
                            return False
            break

        draw(rotated_hunter, new_rect, foods, bombs, score_point, hearts, heal_list, music)
        pygame.display.update()


if __name__ == "__main__":
    playing = True
    while playing:
        playing = main()
    pygame.quit()
