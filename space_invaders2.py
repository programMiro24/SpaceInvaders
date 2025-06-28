import pygame
import sys
# import time
# import os

# инциализация на pygame
pygame.init()
pygame.mixer.init() # Инциализиция на звуковия модел

# размер на прозореца
width = 800
height=600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Invaders")

try:
   icon_image = pygame.image.load("icon.png")
except pygame.error:
    icon_image = None
    print("ВНИМАНИЕ! Изображението icon.png не може да се зареди")

if icon_image:
    pygame.display.set_icon(icon_image)

# Цветове
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (250, 250, 0)
green = (0, 255, 0)

color_screen = (46, 36, 159)
color_player = (255,0,0)
color_bullet = (255,255,255)

# играч
player_width=64
player_hight=64
player_x = width//2 - player_width//2
player_y = height - player_hight - 10
player_speed = 7

# Шрифт за резултат
font = pygame.font.SysFont(None, 36)
score = 0
lives = 3 # Започва с 3 живот(Това са животите)

#bullets
bullets_width=5
bullets_height=10
bullets_speed = 7
bullets=[]

#aliens(izvanzemni)
enemy_width = 32
enemy_height = 32
enemy_color = (0,255,0)
enemy_speed = 4
enemy_direction = 1  # 1 за надясно, -1 за наляво
enemy_drop = 100
rows=3
cols=7
enemies=[]
for row in range(rows):
    for col in range(cols):
        enemy_x = 100 + col * (enemy_width + 20)
        enemy_y = 50 + row * (enemy_height + 20)
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))

# Зареждане на звук
try:
    shoot_sound = pygame.mixer.Sound("lazer.wav")
except pygame.error:
    shoot_sound = None
    print("ВНИМАНИЕ! Звукът lazer.wav не може да бъде зареден.")

try:
    hit_sound = pygame.mixer.Sound("hit.wav")
except pygame.error:
    hit_sound = None
    print("ВНИМАНИЕ! Звукът hit.wav не може да бъде зареден.")

try:
    background_music = pygame.mixer.Sound("space.wav")
except pygame.error:
    background_music = None
    print("ВНИМАНИЕ! Звукът backround.wav не може да бъде зареден.")

if background_music:
    background_music.play()


# Зареждане на изображенията
try:
    player_image = pygame.image.load("spaceship.png")
except pygame.error:
    player_image = None
    print("ВНИМАНИЕ! Изображението spaceship.pnh не може да бъде зареден.")

try:
    enemy_image = pygame.image.load("ufo.png")
except pygame.error:
    enemy_image = None
    print("ВНИМАНИЕ! Изображението spaceship.pnh не може да бъде зареден.")

try:
    background = pygame.image.load("space.png")
except pygame.error:
    background = None
    print("ВНИМАНИЕ! Изображението space.png  не може да бъде зареден.")


# Функция за текст
def draw_screen_text(text, color, y):
    title_text = font.render(text, True, color)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, y))

def exit_screen():
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_END]:
            waiting = False
# Начален екран
def show_start_screen():
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(black)
    draw_screen_text("Space Invaders", white, height // 2 - 40)
    draw_screen_text("Натисни SPACE за старт.", white, height // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def show_game_over_screen():
    screen.fill(black)
    draw_screen_text("КРАЙ НА ИГРАТА.", red, height // 2 - 20)
    draw_screen_text(f"Твоят резултат: {score}", red, height // 2 + 10)
    draw_screen_text("Натисни End за край.", red, height // 2 + 36)
    exit_screen()

def show_win_screen():
    screen.fill(black)
    draw_screen_text("Ти победи.", yellow, height // 2 - 20)
    draw_screen_text(f"Твоят резултат: {score}", white, height // 2 + 10)
    draw_screen_text("Натисни End за край.", white, height // 2 + 36)
    exit_screen()

show_start_screen()
#main loop
clock=pygame.time.Clock()
running = True
while running:
    clock.tick(60)      # 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + player_width//2 - bullets_width//2
                bullet_y = player_y
                bullets.append([bullet_x,bullet_y])
                if shoot_sound:
                    shoot_sound.play()

    #проверка на клавиатурата
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x>0 :
        player_x=player_x-player_speed
    if keys[pygame.K_RIGHT] and player_x<width-player_width:
        player_x=player_x+player_speed

    #obniviavame poziciata na bulletds
    for bullet in bullets:
        bullet[1]=bullet[1]-bullets_speed
    #premahvane na izlezlite izvan ekrana
    bullets=[b for b in bullets if b[1]>0]
    #proverka za udaren vrag ot niakoi snaraid
    bullets_rect=[pygame.Rect(b[0], b[1], bullets_width, bullets_height)for b in bullets]
    new_bullets=[]
    for i,b_rect in enumerate(bullets_rect): # обхожда колекцията със снаряди и връща всеки снаряд и неговият индекс в колекцията
        hit=False
        for e in enemies:
            if e.colliderect(b_rect): # проверява дали врага има обща точка със снаряда b_rect
                hit=True
                score += 10 # Получаваме 10 точки като застреляме врага
                if hit_sound:
                    hit_sound.play()
                enemies.remove(e) # изтриваме врага
                break
        if not hit:
            new_bullets.append(bullets[i])
    bullets = new_bullets

    # местим извънземните по екрана
    move_down = False
    for enemy in enemies:
        enemy.x += enemy_speed * enemy_direction
        if enemy.right >= width or enemy.left <= 0:
            move_down = True

    if move_down:
        enemy_direction *= -1 # сменяме посоката на извънземното
        for enemy in enemies:
            enemy.y += enemy_drop

    # проверка дали враг е достигнал дъното
    for enemy in enemies:
        if enemy.bottom >= player_y:
            enemies.clear()
            enemy_speed += 1
            lives -= 1
            if lives <= 0:
                running = False
                show_game_over_screen()
            else:
                enemy_speed += 1
                for row in range(rows):
                    for col in range(cols):
                        enemy_x = 100 + col * (enemy_width + 20)
                        enemy_y = 50 + row * (enemy_height + 20)
                        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))
            break

    if len(enemies) <= 0:
        show_win_screen()
        break

    #risuvame ekrana
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(color_screen)

    if player_image:
        screen.blit(player_image, (player_x, player_y))
    else:
        pygame.draw.rect(screen,color_player,(player_x,player_y,player_width, player_hight))

    for bullet in bullets:
        pygame.draw.rect(screen, color_bullet, (bullet[0], bullet[1], bullets_width, bullets_height))

    for enemy in enemies:
        if enemy_image:
            screen.blit(enemy_image, (enemy.x, enemy.y))
        else:
            pygame.draw.rect(screen, enemy_color, enemy)

    score_text = font.render(f"Точки: {score}", True, white)
    lives_text = font.render(f"Животи: {lives}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (width - 130, 10))



    pygame.display.flip()


# show_game_over_screen()
pygame.quit()
sys.exit()
