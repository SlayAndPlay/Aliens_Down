import pygame
import random
import math
from pygame import mixer


# Initializing Pygame pkg
pygame.init()
white = (255, 255, 255)

# create game screen
screen = pygame.display.set_mode((800, 600))
bg = pygame.image.load("background1.png")

# Background Music
mixer.music.load("Powerful-Trap-.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("planet.png")
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# Score
score_value = 0
font = pygame.font.Font('bBanter.ttf', 32)

textX = 645
textY = 10

# Game Over Test
game_over_font = pygame.font.Font('bBanter.ttf', 64)
new_game_font = pygame.font.Font('bBanter.ttf', 40)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, white)
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, white)
    new_game_text = new_game_font.render("Play again?", True, white)
    screen.blit(over_text, (245, 250))
    screen.blit(new_game_text, (300, 310))


# Bullet

bullet_image = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
# Ready - bullet cannot be seen
# Fire - bullet is currently moving
bullet_state = 'ready'


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_image, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False

    # Game Loop


running = True

while running:
    # Background Image
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # If keystroke is pressed, check whether it's right or left.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('soundscrate-bullet-ricochet-1.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Applying boundaries

    if playerX <= 0:
        playerX = 0
    elif playerX >= 735:
        playerX = 735
    playerX += playerX_change

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        enemyX += enemyX_change

        # Collision

        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('soundscrate-body-bullet-hit-3.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullets
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
