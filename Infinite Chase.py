import asyncio
import pygame
import sys
import random


pygame.init()
pygame.mixer.init() 

pygame.mixer.music.load(f"sprites/backgroundMusic.mp3")  
pygame.mixer.music.play(loops=-1, start=0.0)  

font = pygame.font.SysFont(None, 33)
clock = pygame.time.Clock()

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jack and Jones's Journey")

pygame.init()

font = pygame.font.SysFont(None, 33)
clock = pygame.time.Clock()

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Infinite Chase")

platform_width = 128
platform_height = 10
platform_list = []
platform_img = pygame.image.load(f"sprites/7tree_top_sprite.png")
num_platforms = 25
floor = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)

character_x = int(SCREEN_WIDTH / 2)
character_y = SCREEN_HEIGHT - 100
gravity = 1
velocity_y = 0
character_size = 50
jump_power = -17
character = pygame.Rect(character_x, character_y, character_size, character_size)
is_jumping = False
character_img = pygame.image.load(f"sprites/jack.png")

follower_x = character_x
follower_y = character_y
follower = pygame.Rect(follower_x, follower_y, character_size, character_size)
follower_delay = 60
follower_positions = []

invincible_time = 7 * 30 
invincible = True
invincible_timer = invincible_time
score = 0
top_score = 0
coin_x, coin_y = int(SCREEN_WIDTH / 2), 50
coin = pygame.Rect(coin_x, coin_y, 50, 50)
Gray = (128, 128, 128)
SKY_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)

is_paused = False
in_home_screen = True
frames_left = 1000
frame = 0

def update_character():
    global character_x, character_y, velocity_y, character, character_img, platform_list, score, follower_x, follower_y, follower, invincible, invincible_timer

    velocity_y += gravity
    character_y += velocity_y
    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_a]:
        character_x -= 5
    elif key_pressed[pygame.K_d]:
        character_x += 5
    character = pygame.Rect(character_x, character_y, character_size, character_size)

    for platform in platform_list:
        if character.colliderect(platform) and velocity_y > 0:
            character_y = platform[1] - character_size
            velocity_y = 0
            if key_pressed[pygame.K_SPACE]:
                velocity_y = jump_power

    if character.colliderect(floor):
        character_y = floor[1] - character_size
        velocity_y = 0
        if key_pressed[pygame.K_SPACE]:
            velocity_y = jump_power
        generate_platforms()

    sprite_frame = int((frame / 5) % 4) + 1
    if len(platform_list) == num_platforms:
        if sprite_frame == 1:
            current_sprite = f"sprites/2character_f1.png"
        elif sprite_frame == 2:
            current_sprite = f"sprites/jack.png"
        elif sprite_frame == 3:
            current_sprite = f"sprites/3character_f3.png"
        else:
            current_sprite = f"sprites/4character_f4.png"
        character_img = pygame.image.load(current_sprite)

    if velocity_y < 0 and len(platform_list) == num_platforms:
        character_img = pygame.image.load(f"sprites/6character_jump_sprite.png")

    if character.colliderect(coin) and len(platform_list) == num_platforms:
        platform_list = []
        character_img = pygame.image.load(f"sprites/5character_happy.png")
        score += 1

    screen.blit(character_img, (character_x, character_y))

    follower_positions.append((character_x, character_y))
    if len(follower_positions) > follower_delay:
        follower_x, follower_y = follower_positions[-follower_delay]
        follower = pygame.Rect(follower_x, follower_y, character_size, character_size)
        screen.blit(character_img, (follower_x, follower_y))

    if not invincible and character.colliderect(follower):
        game_over_display()

    if invincible:
        invincible_timer -= 1
        if invincible_timer <= 0:
            invincible = False

def draw_setting():
    pygame.draw.rect(screen, SKY_BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    for platform in platform_list:
        screen.blit(platform_img, platform)
    pygame.draw.rect(screen, Gray, floor)
    if len(platform_list) == num_platforms:
        coin_img = pygame.image.load(f"sprites/1coin_sprite.png")
        screen.blit(coin_img, (coin_x, coin_y))

    score_txt = font.render(f"Coins Collected: {score}", True, (255, 255, 255))
    screen.blit(score_txt, (10, 10))

def game_over_display():
    global score
    screen.fill(SKY_BLUE)
    game_over_txt = font.render("You Died! Haha!", True, WHITE)
    score_txt = font.render(f"You collected {score} coins", True, WHITE)
    top_score_txt = font.render(f"The highest amount of coins you collected was {top_score}", True, WHITE)
    restart_txt = font.render("Press R to restart, or Q to quit", True, WHITE)

    screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_txt, (SCREEN_WIDTH // 2 - score_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(top_score_txt, (SCREEN_WIDTH // 2 - top_score_txt.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_txt, (SCREEN_WIDTH // 2 - restart_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.update()

    input_waiting = True
    while input_waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    input_waiting = False
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def advance_timer():
    global top_score, frames_left
    frames_left += 1
    if frames_left <= 0:
        if score > top_score:
            top_score = score
        game_over_display()

def generate_platforms():
    current_platform_count = len(platform_list)
    while current_platform_count < num_platforms:
        platform_x = (random.randint(0, SCREEN_WIDTH - platform_width))
        platform_y = (random.randint(80 + (current_platform_count * (SCREEN_HEIGHT - 80) // num_platforms), (80 + (current_platform_count + 1) * (SCREEN_HEIGHT - 80) // num_platforms)))
        platform_list.append(pygame.Rect(platform_x, platform_y, platform_width, platform_height))
        current_platform_count += 1

def reset_variables():
    global frames_left, score, platform_list, character_x, character_y, invincible, invincible_timer
    frames_left = 1000
    score = 0
    platform_list = []
    generate_platforms()
    character_x = int(SCREEN_WIDTH / 2)
    character_y = SCREEN_HEIGHT - 100
    invincible = True
    invincible_timer = invincible_time

def draw_home_screen():
    screen.fill(SKY_BLUE)
    title_text = font.render("Jack and Jones's Journey", True, WHITE)
    start_text = font.render("Press Enter to Start", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

def draw_pause_screen():
    screen.fill(SKY_BLUE)
    pause_text = font.render("Game Paused", True, WHITE)
    resume_text = font.render("Press P to Resume", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)

    screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

def home_screen():
    global frame, is_paused, in_home_screen
    reset_variables()
    running = True
    while running:
        if in_home_screen:
            draw_home_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        in_home_screen = False
                        game_loop()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            continue

        if is_paused:
            draw_pause_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        is_paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = True

        draw_setting()
        update_character()
        pygame.display.update()
        clock.tick(30)
        frame += 1

if score >= 5:
    follower_delay = 30

if score >= 10:
    follower_delay = 15

if score >= 15:
    follower_delay = 10

if score >= 20:
    follower_delay = 5

if score >= 25:
    follower_delay = 0

def game_loop():
    global frame
    reset_variables()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        draw_setting()
        update_character()
        advance_timer()

        pygame.display.update()
        clock.tick(30)
        frame += 1

game_loop()

