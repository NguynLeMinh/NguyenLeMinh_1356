import pygame
import sys

pygame.init()

# Màn hình
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer đơn giản")
clock = pygame.time.Clock()

# Màu
WHITE = (240, 240, 240)
BLUE = (50, 100, 255)
RED = (220, 60, 60)
GREEN = (50, 180, 100)

# Player
player = pygame.Rect(100, 300, 40, 40)
player_speed = 5
jump_power = -12
gravity = 0.6
velocity_y = 0
on_ground = False
attacking = False

# Enemy AI
enemy = pygame.Rect(500, 300, 40, 40)
enemy_speed = 2
enemy_dir = 1
enemy_hp = 5

# Platforms
platforms = [
    pygame.Rect(0, 380, 800, 70),
    pygame.Rect(200, 300, 150, 20),
    pygame.Rect(450, 250, 150, 20)
]

font = pygame.font.SysFont(None, 28)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Di chuyển trái phải
    if keys[pygame.K_a]: player.x -= player_speed
    if keys[pygame.K_d]: player.x += player_speed

    # Nhảy
    if keys[pygame.K_w] and on_ground:
        velocity_y = jump_power
        on_ground = False

    # Đánh
    attacking = keys[pygame.K_SPACE]

    # Trọng lực
    velocity_y += gravity
    player.y += velocity_y

    # Va chạm platform
    on_ground = False
    for p in platforms:
        if player.colliderect(p) and velocity_y >= 0:
            player.bottom = p.top
            velocity_y = 0
            on_ground = True

    # Enemy AI đi qua lại
    enemy.x += enemy_speed * enemy_dir
    if enemy.left < 400 or enemy.right > 760:
        enemy_dir *= -1

    # Đánh enemy
    if attacking and player.colliderect(enemy):
        enemy_hp -= 1

    # Vẽ
    screen.fill(WHITE)

    for p in platforms:
        pygame.draw.rect(screen, GREEN, p)

    pygame.draw.rect(screen, BLUE if not attacking else (255, 150, 0), player)

    if enemy_hp > 0:
        pygame.draw.rect(screen, RED, enemy)
    else:
        screen.blit(font.render("Enemy bị hạ!", True, (0,0,0)), (350, 200))

    screen.blit(font.render(f"Enemy HP: {enemy_hp}", True, (0,0,0)), (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
