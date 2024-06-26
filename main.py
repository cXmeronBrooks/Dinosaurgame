import pygame
import random

pygame.init()
pygame.font.init()

dinosaur_sprite = pygame.image.load(r"dinoimage.png")
dinosaur_sprit = pygame.transform.scale(dinosaur_sprite, (64,64))

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
FPS = 60
WIDTH = 640
HEIGHT = 640

s = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20)
run = True
score = 0
died = False
final_score = 0
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 40
        self.width = 20
        self.speed = 10
    def draw(self):
        pygame.draw.rect(s,RED, (self.x, self.y, self.width, self.height))
    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = WIDTH + random.randint(0,100)
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.speed = 3
        self.jump_counter = 10
        self.jumping = False
        self.y_vel = 0
    def draw(self):
        s.blit(dinosaur_sprit, (self.x, self.y))
        #pygame.draw.rect(s, BLUE, (self.x, self.y, self.width, self.height))
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.y_vel = -15
    def update(self):
        if self.jumping:
            self.y_vel += 1
            self.y += self.y_vel
            if self.y >= HEIGHT - 100 - self.height:
                self.y = HEIGHT - 100 - self.height
                self.jumping = False
                self.y_vel = 0

player = Player(40,WIDTH - 100 - 64)
obstacles = [Obstacle(WIDTH + i*300, HEIGHT - 100 - 40) for i in range(2)]
def draw_ground():
    pygame.draw.rect(s, BLACK, (0, HEIGHT- 100, WIDTH, HEIGHT))

def check_collision(player, obstacles):
    for obstacle in obstacles:
        if player.x < obstacle.x + obstacle.width and player.x + player.width > obstacle.x:
            if player.y + player.height > obstacle.y:
                return True
    return False
def update_screen(score):
    player.update()
    s.fill(WHITE)
    draw_ground()
    if not died:
        player.draw()
        for obstacle in obstacles:
            obstacle.draw()
    score_text = font.render(f'Score: {score}', True, BLACK)
    if died:
        s.blit(font.render("YOU DIED. SCORE: " + str(final_score), True, BLACK), (200, 200))
    else:
        s.blit(score_text, (10, 10))
    pygame.display.flip()

while run:
    clock.tick(FPS)
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if key[pygame.K_d] and player.x + player.width < WIDTH:
        player.x += player.speed
    if key[pygame.K_a] and player.x > 0:
        player.x -= player.speed
    if key[pygame.K_SPACE]:
        player.jump()

    for obstacle in obstacles:
        obstacle.update()

    if check_collision(player, obstacles) and not died:
        died = True
        final_score = score



    score += 1
    update_screen(score)
