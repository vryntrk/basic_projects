import pygame
import random
import time

pygame.init()
font = pygame.font.SysFont('Orbitron', 30)

height = 1024
width = 1024

background = pygame.transform.scale(pygame.image.load("background.png"), (width, height))

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Runner")
icon = pygame.image.load("game.png")
pygame.display.set_icon(icon)

alien_width = 50
alien_height = 50
alien_vel = 4
alien = pygame.transform.scale(pygame.image.load("alien.png"), (alien_width, alien_height))
alien_coordinate = alien.get_rect()
alien_coordinate.x = 0
alien_coordinate.y = height - alien_height

spaceship_width = 150
spaceship_height = 150
spaceship = pygame.transform.scale(pygame.image.load("spaceship.png"), (spaceship_width, spaceship_height))
spaceship_coordinate = spaceship.get_rect()
spaceship_coordinate.x = (width - spaceship_width) // 2
spaceship_coordinate.y = spaceship_height
spaceship_mask = pygame.mask.from_surface(spaceship)

shop_width = 250
shop_height = 250
shop = pygame.transform.scale(pygame.image.load("shop.png"), (shop_width, shop_height))
shop_coordinate = shop.get_rect()
shop_coordinate.x = (width - shop_width) // 2
shop_coordinate.y = (height - shop_height) // 2
shop_mask = pygame.mask.from_surface(shop)

coin_width = 20
coin_height = 20
coin = pygame.transform.scale(pygame.image.load("coin.png"), (coin_width, coin_height))
coin_coordinate = coin.get_rect()

coin_sound = pygame.mixer.Sound("coin_receive.mp3")
buying_sound = pygame.mixer.Sound("purchase.mp3")
fixing_sound = pygame.mixer.Sound("fix.mp3")

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1, 0.0)


def borders(alien_rect, alien_mask):
    offset_shop = (shop_coordinate.x - alien_rect.x, shop_coordinate.y - alien_rect.y)
    offset_spaceship = (spaceship_coordinate.x - alien_rect.x, spaceship_coordinate.y - alien_rect.y)
    if alien_mask.overlap(shop_mask, offset_shop) or alien_mask.overlap(spaceship_mask, offset_spaceship):
        return True
    return False


def happy_end():
    end_message = font.render("CONGRATS, YOU DID IT", 1, "white")
    window.blit(end_message, ((width - end_message.get_width()) // 2, (height - end_message.get_height()) // 2))
    pygame.display.update()


def available():
    column_1 = random.randint(0, 387 - coin_width)
    column_2 = random.randint(637 + coin_width, width - coin_width)
    columns = [column_1, column_2]
    selected_column = random.choice(columns)
    return selected_column


def draw(alien_img, coins, total_coin, battery_price, required_battery):
    window.blit(background, (0, 0))

    pygame.draw.line(window, "white", (0, 95), (width, 95), 5)
    pygame.draw.line(window, "white", (115, 0), (115, 95), 5)
    pygame.draw.line(window, "white", (width - 115, 0), ( width - 115, 95), 5)

    header_part1 = font.render("SPACE", 1, "green")
    window.blit(header_part1, ((115 - header_part1.get_width()) // 2, (100 - header_part1.get_height()) // 2))

    header_part2 = font.render("RUNNER", 1, "green")
    window.blit(header_part2, ((115 - header_part2.get_width()) // 2 + 909, (100 - header_part2.get_height()) // 2))

    all_coins = font.render(f"COINS: {total_coin}", 1, "white")
    window.blit(all_coins, ((512 - all_coins.get_width()) // 2, (100 - all_coins.get_height()) // 2))

    fee = font.render(f"PRICE: {battery_price}", 1, "white")
    window.blit(fee, ((width - fee.get_width()) // 2, (100 - fee.get_height()) // 2))

    required = font.render(f"REQUIRED: {required_battery}", 1, "white")
    window.blit(required, ((width + 3 * required.get_width()) // 2, (100 - required.get_height()) // 2))

    window.blit(alien_img, (alien_coordinate.x, alien_coordinate.y))
    window.blit(spaceship, (spaceship_coordinate.x, spaceship_coordinate.y))
    window.blit(shop, (shop_coordinate.x, shop_coordinate.y))

    for c in coins:
        window.blit(coin, c[0])

    pygame.display.update()


def main():
    run = True

    clock = pygame.time.Clock()

    angle = 0
    global alien_coordinate

    coin_add_increment = 3000
    coin_count = 0
    coins = []

    total_coin = 0
    battery_price = 5
    required_battery = 5

    received_battery = False

    while run:
        dt = clock.tick(60)
        coin_count += dt

        elapsed = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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

        rotated_alien = pygame.transform.rotate(alien, angle)
        center = alien_coordinate.center
        alien_coordinate = rotated_alien.get_rect()
        alien_coordinate.center = center
        alien_mask = pygame.mask.from_surface(rotated_alien)

        if keys[pygame.K_LEFT] and alien_coordinate.x > 0:
            alien_coordinate.x -= alien_vel
            if borders(alien_coordinate, alien_mask):
                alien_coordinate.x += alien_vel

        if keys[pygame.K_RIGHT] and alien_coordinate.x < width - alien_width:
            alien_coordinate.x += alien_vel
            if borders(alien_coordinate, alien_mask):
                alien_coordinate.x -= alien_vel

        if keys[pygame.K_UP] and alien_coordinate.y > 100:
            alien_coordinate.y -= alien_vel
            if borders(alien_coordinate, alien_mask):
                alien_coordinate.y += alien_vel

        if keys[pygame.K_DOWN] and alien_coordinate.y < height - alien_height:
            alien_coordinate.y += alien_vel
            if borders(alien_coordinate, alien_mask):
                alien_coordinate.y -= alien_vel

        if coin_count >= coin_add_increment:
            for _ in range(3):
                coin_coordinate.x = available()
                coin_coordinate.y = random.randint(100, height - coin_height)
                coin_rect = pygame.Rect(coin_coordinate.x, coin_coordinate.y, coin_width, coin_height)
                new_coin = [coin_rect, elapsed]
                coins.append(new_coin)
            coin_count = 0
            coin_add_increment = 3000

        for c in coins[:]:
            if alien_coordinate.colliderect(c[0]):
                coin_sound.play()
                coins.remove(c)
                total_coin += 1
            else:
                if elapsed - c[1] > 5:
                    coins.remove(c)

        interaction_box = alien_coordinate.inflate(10, 10)
        if interaction_box.colliderect(shop_coordinate) and not received_battery and total_coin - battery_price >= 0:
            buying_sound.play()
            received_battery = True
            total_coin -= battery_price
            battery_price += 2

        if interaction_box.colliderect(spaceship_coordinate) and received_battery:
            fixing_sound.play()
            received_battery = False
            required_battery -= 1
            if required_battery == 0:
                pygame.mixer.music.stop()
                happy_end()
                pygame.time.delay(3000)
                run = False

        draw(rotated_alien, coins, total_coin, battery_price, required_battery)
    pygame.quit()


main()
