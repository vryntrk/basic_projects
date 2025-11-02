import pygame
import random
import time

pygame.init()

width = 1024
height = 1024

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Eater")
icon = pygame.image.load("game.png")
pygame.display.set_icon(icon)

background = pygame.transform.scale(pygame.image.load("sea.png"), (width, height))

hunter_width = 100
hunter_height = 50
hunter_vel = 4
hunter_img = pygame.image.load("shark.png")
hunter = pygame.transform.scale(hunter_img, (hunter_width, hunter_height))
hunter_coordinate = hunter.get_rect()
hunter_coordinate.x = (width - hunter_width) // 2
hunter_coordinate.y = (height - hunter_height) // 2

food_width = 60
food_height = 30
food_img = pygame.image.load("salmon.png")
food = pygame.transform.scale(food_img, (food_width, food_height))
food_coordinate = food.get_rect()

bomb_width = 50
bomb_height = 50
bomb_img = pygame.image.load("bomb.png")
bomb = pygame.transform.scale(bomb_img, (bomb_width, bomb_height))
bomb_coordinate = bomb.get_rect()

heal_width = 50
heal_height = 50
heal_img = pygame.image.load("heart.png")
heal = pygame.transform.scale(heal_img, (heal_width, heal_height))
heal_coordinate = heal.get_rect()

font = pygame.font.SysFont("consolas", 32)

eat_sound = pygame.mixer.Sound("eat.mp3")
damage_sound = pygame.mixer.Sound("explosion.mp3")
upgrade_sound = pygame.mixer.Sound("upgrade.mp3")
heal_sound = pygame.mixer.Sound("heal.mp3")

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1, 0.0)


def draw(foods, bombs, score_point, hearts, heal_list):
    win.blit(background, (0, 0))
    pygame.draw.line(win, "white", (0, 95), (width, 95), 5)

    win.blit(hunter, (hunter_coordinate.x, hunter_coordinate.y))

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

    pygame.display.update()


def the_end(score_point):
    message_1 = font.render("Game Over!", 1, "White")
    win.blit(message_1, ((width - message_1.get_width()) // 2, height // 2 - message_1.get_height() - 10))

    message_2 = font.render(f"Your Score: {score_point}", 1, "White")
    win.blit(message_2, ((width - message_2.get_width()) // 2, (height - message_2.get_height()) // 2))

    pygame.display.update()


def main():
    global hunter, hunter_coordinate, hunter_width, hunter_height
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

    while run:
        dt = clock.tick(120)
        food_count += dt
        bomb_count += dt
        heal_count += dt

        elapsed_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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
            if hunter_coordinate.colliderect(f[0]):
                eat_sound.play()
                foods.remove(f)
                score_point += 50
            else:
                if elapsed_time - f[1] > 5:
                    foods.remove(f)

        if score_point == growth_point:
            upgrade_sound.play()

            previous_center = hunter_coordinate.center

            hunter_width += 20
            hunter_height += 10

            hunter = pygame.transform.scale(hunter_img, (hunter_width, hunter_height))
            hunter_coordinate = hunter.get_rect()
            hunter_coordinate.center = previous_center

            growth_point += 750

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
            if hunter_coordinate.colliderect(b[0]):
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
            if hunter_coordinate.colliderect(h[0]):
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
            run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and hunter_coordinate.left > 0:
            hunter_coordinate.x -= hunter_vel
        if keys[pygame.K_RIGHT] and hunter_coordinate.right < width:
            hunter_coordinate.x += hunter_vel
        if keys[pygame.K_UP] and hunter_coordinate.top > 100:
            hunter_coordinate.y -= hunter_vel
        if keys[pygame.K_DOWN] and hunter_coordinate.bottom < height:
            hunter_coordinate.y += hunter_vel

        draw(foods, bombs, score_point, hearts, heal_list)

    pygame.quit()


main()
