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
font = pygame.font.SysFont("Ocraextended", 30)

height = 800
width = 800

background = pygame.transform.scale(pygame.image.load("pictures/background.png"), (width, height))

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Runner")
icon = pygame.image.load("pictures/logo.png")
pygame.display.set_icon(icon)

alien_width = 40
alien_height = 40
alien_vel = 4
alien = pygame.transform.scale(pygame.image.load("pictures/alien.png"), (alien_width, alien_height))
alien_coordinate = alien.get_rect()
alien_coordinate.x = 0
alien_coordinate.y = height - alien_height

spaceship_width = 100
spaceship_height = 100
spaceship = pygame.transform.scale(pygame.image.load("pictures/spaceship.png"), (spaceship_width, spaceship_height))
spaceship_coordinate = spaceship.get_rect()
spaceship_coordinate.x = (width - spaceship_width) // 2
spaceship_coordinate.y = 50 + spaceship_height
spaceship_mask = pygame.mask.from_surface(spaceship)

shop_width = 200
shop_height = 200
shop = pygame.transform.scale(pygame.image.load("pictures/shop.png"), (shop_width, shop_height))
shop_coordinate = shop.get_rect()
shop_coordinate.x = (width - shop_width) // 2
shop_coordinate.y = (height - shop_height) // 2
shop_mask = pygame.mask.from_surface(shop)

coin_width = 15
coin_height = 15
coin = pygame.transform.scale(pygame.image.load("pictures/coin.png"), (coin_width, coin_height))
coin_coordinate = coin.get_rect()

spacecraft_width = 100
spacecraft_height = 100
spacecraft_vel = 5
spacecraft = pygame.transform.scale(pygame.image.load("pictures/spacecraft.png"), (spacecraft_width, spacecraft_height))
spacecraft_coordinate = spacecraft.get_rect()
spacecraft_mask = pygame.mask.from_surface(spacecraft)

battleship_width = 100
battleship_height = 100
battleship_vel = 5
battleship = pygame.transform.scale(pygame.image.load("pictures/battleship.png"), (battleship_width, battleship_height))
battleship_coordinate = battleship.get_rect()
battleship_mask = pygame.mask.from_surface(battleship)

life_level_width = 90
life_level_height = 90
life0 = pygame.transform.scale(pygame.image.load("pictures/life0.png"), (life_level_width, life_level_height))
life1 = pygame.transform.scale(pygame.image.load("pictures/life1.png"), (life_level_width, life_level_height))
life2 = pygame.transform.scale(pygame.image.load("pictures/life2.png"), (life_level_width, life_level_height))
life3 = pygame.transform.scale(pygame.image.load("pictures/life3.png"), (life_level_width, life_level_height))
life4 = pygame.transform.scale(pygame.image.load("pictures/life4.png"), (life_level_width, life_level_height))
life5 = pygame.transform.scale(pygame.image.load("pictures/life5.png"), (life_level_width, life_level_height))
all_lives = [life0, life1, life2, life3, life4, life5]

battery_width = 90
battery_height = 90
battery_on = pygame.transform.scale(pygame.image.load("pictures/battery_on.png"), (battery_width, battery_height))
battery_off = pygame.transform.scale(pygame.image.load("pictures/battery_off.png"), (battery_width, battery_height))

coin_sound = pygame.mixer.Sound("sounds/coin_receive.mp3")
buying_sound = pygame.mixer.Sound("sounds/purchase.mp3")
fixing_sound = pygame.mixer.Sound("sounds/fix.mp3")
crash_sound = pygame.mixer.Sound("sounds/crash.mp3")
drop_sound = pygame.mixer.Sound("sounds/coin_drop.mp3")
pygame.mixer.music.load("sounds/background.mp3")


def borders(alien_rect, alien_mask):
    offset_shop = (shop_coordinate.x - alien_rect.x, shop_coordinate.y - alien_rect.y)
    offset_spaceship = (spaceship_coordinate.x - alien_rect.x, spaceship_coordinate.y - alien_rect.y)
    if alien_mask.overlap(shop_mask, offset_shop) or alien_mask.overlap(spaceship_mask, offset_spaceship):
        return True
    return False


def music_on():
    music_on_text = font.render("Music On (M)", 1, "White")
    window.blit(music_on_text, ((width - music_on_text.get_width()) // 2, 0))


def music_off():
    music_off_text = font.render("Music Off (M)", 1, "White")
    window.blit(music_off_text, ((width - music_off_text.get_width()) // 2, 0))


def happy_end():
    end_message = font.render("DONE! PRESS 'R' TO RESTART OR 'ESC' TO QUIT.", 1, "white")
    window.blit(end_message, ((width - end_message.get_width()) // 2, (height - end_message.get_height()) // 2))
    pygame.display.update()


def sad_end():
    end_message = font.render("FAIL! PRESS 'R' TO RESTART OR 'ESC' TO QUIT.", 1, "white")
    window.blit(end_message, ((width - end_message.get_width()) // 2, (height - end_message.get_height()) // 2))
    pygame.display.update()


def available():
    column_1 = random.randint(0, 300 - coin_width)
    column_2 = random.randint(500 + coin_width, width - coin_width)
    columns = [column_1, column_2]
    selected_column = random.choice(columns)
    return selected_column


def draw(alien_img, coins, life_level, total_coin, battery_price, required_battery, battery, battleships, spacecrafts, music):
    window.blit(background, (0, 0))

    pygame.draw.line(window, "white", (0, 95), (width, 95), 5)

    window.blit(life_level, (5, (100 - life_level.get_height()) // 2))
    window.blit(battery, (width - battery.get_width() - 5, (100 - battery.get_height()) // 2))

    all_coins = font.render(f"COINS: {total_coin}", 1, "white")
    window.blit(all_coins, ((0.5 * width - all_coins.get_width()) // 2, (100 - all_coins.get_height()) // 2))

    fee = font.render(f"PRICE: {battery_price}", 1, "white")
    window.blit(fee, ((width - fee.get_width()) // 2, (100 - fee.get_height()) // 2))

    required = font.render(f"REQUIRED: {required_battery}", 1, "white")
    window.blit(required, ((1.5 * width - required.get_width()) // 2, (100 - required.get_height()) // 2))

    window.blit(alien_img, (alien_coordinate.x, alien_coordinate.y))
    window.blit(spaceship, (spaceship_coordinate.x, spaceship_coordinate.y))
    window.blit(shop, (shop_coordinate.x, shop_coordinate.y))

    for c in coins:
        window.blit(coin, c[0])

    for b in battleships:
        window.blit(battleship, b)

    for s in spacecrafts:
        window.blit(spacecraft, s)

    if music:
        music_on()
    else:
        music_off()


def main():
    run = True

    clock = pygame.time.Clock()

    angle = 0
    global alien_coordinate
    global battleship_vel
    global spacecraft_vel

    coin_add_increment = 3000
    coin_count = 0
    coins = []

    battleship_add_increment = 4000
    battleship_count = 0
    battleships = []

    spacecraft_add_increment = 4000
    spacecraft_count = 0
    spacecrafts = []

    total_coin = 0
    battery_price = 5
    required_battery = 5

    received_battery = False

    life_count = 5

    music = True
    if music:
        pygame.mixer.music.play(-1, 0.0)

    while run:
        dt = clock.tick(60)
        coin_count += dt
        battleship_count += dt
        spacecraft_count += dt

        elapsed = time.time()

        hit = False

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

        if battleship_count >= battleship_add_increment:
            for _ in range(1):
                battleship_coordinate.x = 550
                battleship_rect = pygame.Rect(battleship_coordinate.x, -battleship_height, battleship_width, battleship_height)
                battleships.append(battleship_rect)
            battleship_count = 0
            battleship_add_increment = max(2000, battleship_add_increment - 500)
            battleship_vel = max(8.0, battleship_vel + 0.25)

        for b in battleships[:]:
            b.y += battleship_vel
            offset = (b.x - alien_coordinate.x, b.y - alien_coordinate.y)
            if b.y > height:
                battleships.remove(b)
            elif alien_mask.overlap(battleship_mask, offset):
                hit = True
                alien_coordinate.x = 0
                alien_coordinate.y = height - alien_height

        if spacecraft_count >= spacecraft_add_increment:
            for _ in range(1):
                spacecraft_coordinate.x = 150
                spacecraft_rect = pygame.Rect(spacecraft_coordinate.x, height-spacecraft_height, spacecraft_width, spacecraft_height)
                spacecrafts.append(spacecraft_rect)
            spacecraft_count = 0
            spacecraft_add_increment = max(2000, spacecraft_add_increment - 500)
            spacecraft_vel = max(8.0, spacecraft_vel + 0.25)

        for s in spacecrafts[:]:
            s.y -= spacecraft_vel
            offset = (s.x - alien_coordinate.x, s.y - alien_coordinate.y)
            if s.y < 0:
                spacecrafts.remove(s)
            elif alien_mask.overlap(spacecraft_mask, offset):
                hit = True
                alien_coordinate.x = 0
                alien_coordinate.y = height - alien_height

        if hit:
            crash_sound.play()
            life_count -= 1
            if total_coin > 0:
                drop_sound.play()
                total_coin = 0
            if life_count == 0:
                pygame.mixer.music.stop()
                sad_end()
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

        battery = battery_on if received_battery else battery_off
        current_life = all_lives[life_count]
        draw(rotated_alien, coins, current_life, total_coin, battery_price, required_battery, battery, battleships, spacecrafts, music)

        pygame.display.update()


if __name__ == "__main__":
    playing = True
    while playing:
        playing = main()
    pygame.quit()
