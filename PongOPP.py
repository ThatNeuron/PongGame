import pygame
import random

# Initialize the game
pygame.init()

# Create class for player
class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width,height])
        
        pygame.draw.rect(self.image, color, [0,0,width,height])

        self.rect = self.image.get_rect()

    def moveUP(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDOWN(self, pixels):
        self.rect.y += pixels
        if self.rect.y > HEIGHT- 120:
            self.rect.y = HEIGHT - 120

# create class for the ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([20,20])

        pygame.draw.rect(self.image, RED,[0, 0 ,20,20])
        self.velocity = [random.randint(4,8), random.randint(1,8)]

        self.rect = self.image.get_rect()

    def init_position(self):
        self.rect.x = (WIDTH/2)-10
        self.rect.y = (HEIGHT/2)-10

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]

# Setup the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Pong')

# Setup the colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
TN = (210,210,210)

score = [0,0]

player1 = Player(BLACK, 20, 120)
player1.rect.x = WIDTH - 25
player1.rect.y = (HEIGHT / 2) - 60
player2 = Player(BLACK, 20, 120)
player2.rect.x = 5
player2.rect.y = (HEIGHT / 2) - 60

ball = Ball()
ball.init_position()

allSprites = pygame.sprite.Group()

allSprites.add(player1)
allSprites.add(player2)
allSprites.add(ball)

collistionTolerance = 10

# Setup the clock
FPS = 60
clock = pygame.time.Clock()

# Main loop of the game
gameActive = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        gameActive= True
    if keys[pygame.K_UP]:
        player1.moveUP(5)
    if keys[pygame.K_DOWN]:
        player1.moveDOWN(5)
    if keys[pygame.K_z]:
        player2.moveUP(5)
    if keys[pygame.K_s]:
        player2.moveDOWN(5)

    if gameActive:
        allSprites.update()
        if ball.rect.y <= 0 or ball.rect.y >= HEIGHT-20:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.x <= 0 :
            score[1] += 1
            print(score)
            ball.init_position()
            gameActive = False
        if ball.rect.x >= WIDTH-20:
            score[0] += 1
            print(score)
            ball.init_position()
            gameActive = False
    if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
        print('here')
        if abs(player1.rect.left - ball.rect.right) < collistionTolerance or abs(player2.rect.right - ball.rect.left) < collistionTolerance:
            ball.bounce()
        if abs(player1.rect.top - ball.rect.bottom) < collistionTolerance or abs(player2.rect.top - ball.rect.bottom) < collistionTolerance or abs(player1.rect.bottom - ball.rect.top) < collistionTolerance or abs(player2.rect.bottom - ball.rect.top) < collistionTolerance:
            ball.velocity[1] = -ball.velocity[1]

    # Fill the screen
    screen.fill(TN)

    allSprites.draw(screen)

    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(score[0]), 5, (200,50,0))
    screen.blit(text, (195,10))
    text = font.render(str(score[1]), 5, (200,50,0))
    screen.blit(text, (600,10))

    # Update the game
    pygame.display.update()

    # Tick the clock
    clock.tick(FPS)

# Quit the game
pygame.quit()