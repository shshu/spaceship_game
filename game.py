import random
import os

import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
ENEMY_IMAGE_PATH = os.path.join(BASE_PATH, 'image', 'enemy.png')
ENEMY_IMAGE_FILE = pygame.image.load(ENEMY_IMAGE_PATH)
ENEMY_IMAGE_PATH = os.path.join(BASE_PATH, 'image', 'ship.png')
SHIP_IMAGE_FILE = pygame.image.load(ENEMY_IMAGE_PATH)
BACKGROUND_IMG_PATH = os.path.join(BASE_PATH, 'image', 'bg.png')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = SHIP_IMAGE_FILE
        self.surf = pygame.Surface(
            (self.image.get_width(), self.image.get_height()))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Enforce player always on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = ENEMY_IMAGE_FILE
        self.surf = pygame.Surface(
            (self.image.get_height(), self.image.get_width()))
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH + self.image.get_width(),
                    random.randint(
                        int(self.image.get_height() /
                            2), int(SCREEN_HEIGHT -
                                    self.image.get_height() / 2))))
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(player.rect.right,
                    (player.rect.bottom + player.rect.top) / 2))
        self.speed = 10
        self.image = self.surf

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


def run():

    # Initialize
    pygame.display.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load(BACKGROUND_IMG_PATH).convert()

    player = Player()

    # Create sprite groups
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    shooting = pygame.sprite.Group()

    # Create a custom event for adding a new enemy.
    ADDENEMY = pygame.USEREVENT + 1
    # Decrease timer for level up logic
    pygame.time.set_timer(ADDENEMY, 500)

    running = True
    while running:

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                # space is pressed create a bullet
                if event.key == K_SPACE:
                    bullet = Bullet(player)
                    shooting.add(bullet)
                    all_sprites.add(bullet)

            # add enemy event
            elif event.type == ADDENEMY:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)

        screen.blit(background, (0, 0))
        pressed_keys = pygame.key.get_pressed()

        # update the player sprite based on user keypresses
        player.update(pressed_keys)

        # update auto move for bullets and enemies
        enemies.update()
        shooting.update()

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        # player lose
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            running = False

        pygame.sprite.groupcollide(shooting, enemies, True, True)

        # Update the display
        pygame.display.flip()

        # Update game speed
        clock.tick(30)

    pygame.display.quit()


run()
