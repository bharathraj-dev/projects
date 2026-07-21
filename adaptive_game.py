import pygame
import random
import time
import os

pygame.init()

# =========================
# WINDOW
# =========================
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adaptive Difficulty Game")

clock = pygame.time.Clock()

# =========================
# SCORE FILE
# =========================
HIGH_SCORE_FILE = "highscore.txt"

if not os.path.exists(HIGH_SCORE_FILE):

    with open(HIGH_SCORE_FILE, "w") as file:
        file.write("0")

# =========================
# COLORS
# =========================
WHITE = (255, 255, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 120)
BLACK = (15, 15, 15)
BLUE = (100, 180, 255)

# =========================
# PLAYER
# =========================
player_size = 50

player_x = WIDTH // 2
player_y = HEIGHT - 80

player_speed = 7

# =========================
# ENEMIES
# =========================
enemy_size = 40

enemies = []

enemy_speed = 4
spawn_rate = 30

# =========================
# GAME DATA
# =========================
score = 0

difficulty_level = 1

start_time = time.time()

# Player analytics
dodged_enemies = 0
player_moves = 0

font = pygame.font.SysFont("Arial", 28)

# =========================
# SCORE FUNCTIONS
# =========================

def load_high_score():

    with open(HIGH_SCORE_FILE, "r") as file:
        return int(file.read())


def save_high_score(new_score):

    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(new_score))


# =========================
# FUNCTIONS
# =========================

def create_enemy():

    x = random.randint(0, WIDTH - enemy_size)

    y = -enemy_size

    enemies.append([x, y])


def draw_player():

    pygame.draw.rect(
        screen,
        BLUE,
        (player_x, player_y, player_size, player_size)
    )


def draw_enemies():

    for enemy in enemies:

        pygame.draw.rect(
            screen,
            RED,
            (enemy[0], enemy[1], enemy_size, enemy_size)
        )


def move_enemies():

    global score
    global dodged_enemies

    for enemy in enemies[:]:

        enemy[1] += enemy_speed

        # Enemy passed player
        if enemy[1] > HEIGHT:

            enemies.remove(enemy)

            score += 1

            dodged_enemies += 1


def check_collision():

    player_rect = pygame.Rect(
        player_x,
        player_y,
        player_size,
        player_size
    )

    for enemy in enemies:

        enemy_rect = pygame.Rect(
            enemy[0],
            enemy[1],
            enemy_size,
            enemy_size
        )

        if player_rect.colliderect(enemy_rect):
            return True

    return False


def adaptive_difficulty():

    global enemy_speed
    global spawn_rate
    global difficulty_level

    survival_time = time.time() - start_time

    # =========================
    # PERFORMANCE METRIC
    # =========================

    performance_score = (
        score +
        dodged_enemies * 0.5 +
        survival_time * 0.2
    )

    # =========================
    # ADAPTIVE AI
    # =========================

    if performance_score > 40:

        difficulty_level = 5

        enemy_speed = 10

        spawn_rate = 12

    elif performance_score > 30:

        difficulty_level = 4

        enemy_speed = 8

        spawn_rate = 16

    elif performance_score > 20:

        difficulty_level = 3

        enemy_speed = 7

        spawn_rate = 20

    elif performance_score > 10:

        difficulty_level = 2

        enemy_speed = 5

        spawn_rate = 25

    else:

        difficulty_level = 1

        enemy_speed = 4

        spawn_rate = 30


def draw_ui():

    survival_time = int(time.time() - start_time)

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    diff_text = font.render(
        f"Difficulty: {difficulty_level}",
        True,
        GREEN
    )

    time_text = font.render(
        f"Time: {survival_time}s",
        True,
        WHITE
    )

    high_score_text = font.render(
        f"High Score: {load_high_score()}",
        True,
        BLUE
    )

    screen.blit(score_text, (20, 20))

    screen.blit(diff_text, (20, 60))

    screen.blit(time_text, (20, 100))

    screen.blit(high_score_text, (20, 140))


# =========================
# GAME OVER SCREEN
# =========================

def game_over():

    global enemies
    global score
    global difficulty_level
    global enemy_speed
    global spawn_rate
    global player_x
    global dodged_enemies
    global start_time
    global frame_count
    global player_moves

    # =========================
    # SAVE HIGH SCORE
    # =========================

    high_score = load_high_score()

    if score > high_score:

        high_score = score

        save_high_score(high_score)

    over_font = pygame.font.SysFont("Arial", 60)

    button_font = pygame.font.SysFont("Arial", 35)

    small_font = pygame.font.SysFont("Arial", 28)

    while True:

        screen.fill(BLACK)

        # =========================
        # GAME OVER TEXT
        # =========================

        text = over_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(text, (WIDTH // 2 - 180, 70))

        # =========================
        # SCORE DISPLAY
        # =========================

        current_score_text = small_font.render(
            f"Current Score: {score}",
            True,
            WHITE
        )

        high_score_text = small_font.render(
            f"Highest Score: {high_score}",
            True,
            GREEN
        )

        screen.blit(current_score_text, (280, 160))

        screen.blit(high_score_text, (280, 210))

        # =========================
        # BUTTONS
        # =========================

        play_button = pygame.Rect(250, 300, 300, 70)

        score_button = pygame.Rect(250, 390, 300, 70)

        exit_button = pygame.Rect(250, 480, 300, 70)

        pygame.draw.rect(screen, GREEN, play_button)

        pygame.draw.rect(screen, BLUE, score_button)

        pygame.draw.rect(screen, RED, exit_button)

        # =========================
        # BUTTON TEXT
        # =========================

        play_text = button_font.render(
            "PLAY AGAIN",
            True,
            BLACK
        )

        score_text = button_font.render(
            "VIEW SCORE",
            True,
            WHITE
        )

        exit_text = button_font.render(
            "EXIT",
            True,
            WHITE
        )

        screen.blit(play_text, (295, 320))

        screen.blit(score_text, (295, 410))

        screen.blit(exit_text, (360, 500))

        pygame.display.update()

        # =========================
        # EVENTS
        # =========================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()

                # =========================
                # PLAY AGAIN
                # =========================

                if play_button.collidepoint(mouse_pos):

                    enemies.clear()

                    score = 0

                    difficulty_level = 1

                    enemy_speed = 4

                    spawn_rate = 30

                    player_x = WIDTH // 2

                    dodged_enemies = 0

                    player_moves = 0

                    start_time = time.time()

                    frame_count = 0

                    return

                # =========================
                # VIEW SCORE
                # =========================

                if score_button.collidepoint(mouse_pos):

                    print("\n========== PLAYER DATA ==========")

                    print("Current Score:", score)

                    print("Highest Score:", high_score)

                    print("Difficulty Reached:", difficulty_level)

                    print("Enemies Dodged:", dodged_enemies)

                    print("Player Moves:", player_moves)

                    print("=================================\n")

                # =========================
                # EXIT
                # =========================

                if exit_button.collidepoint(mouse_pos):

                    pygame.quit()

                    quit()


# =========================
# MAIN LOOP
# =========================

running = True

frame_count = 0

while running:

    clock.tick(60)

    screen.fill(BLACK)

    # =========================
    # EVENTS
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    # =========================
    # KEYBOARD INPUT
    # =========================

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > 0:

        player_x -= player_speed

        player_moves += 1

    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:

        player_x += player_speed

        player_moves += 1

    # =========================
    # CREATE ENEMIES
    # =========================

    if frame_count % spawn_rate == 0:

        create_enemy()

    # =========================
    # UPDATE
    # =========================

    move_enemies()

    adaptive_difficulty()

    # =========================
    # DRAW
    # =========================

    draw_player()

    draw_enemies()

    draw_ui()

    # =========================
    # COLLISION
    # =========================

    if check_collision():

        game_over()

    pygame.display.update()

    frame_count += 1

pygame.quit()