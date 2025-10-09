"""
Basic 2D Battle Royale Style Game using Pygame

Features:
- Player movement with arrow keys or WASD
- Shooting bullets with space bar
- Simple enemies moving randomly or chasing player
- Health system for player and enemies
- Collision detection between bullets and enemies
- Game over condition when player health reaches zero
- Simple shapes for all entities
"""

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
GRAY = (169, 169, 169)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basic 2D Battle Royale")

# Clock for FPS control
clock = pygame.time.Clock()
FPS = 60  # Frames per second


class Player:
    """ Player class that can move and shoot """
    def __init__(self):
        # Starting position at center bottom
        self.width = 40
        self.height = 40
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.color = BLUE
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shoot_cooldown = 0  # Frames until next shot allowed

    def handle_movement(self, keys_pressed):
        # Move player based on pressed keys
        if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and self.x - self.speed > 0:
            self.x -= self.speed
        if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and self.x + self.speed + self.width < SCREEN_WIDTH:
            self.x += self.speed
        if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and self.y - self.speed > 0:
            self.y -= self.speed
        if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and self.y + self.speed + self.height < SCREEN_HEIGHT:
            self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def shoot(self, bullets):
        # Shoot a bullet if cooldown allows
        if self.shoot_cooldown == 0:
            # Bullet spawns from center top of player
            bullet = Bullet(self.x + self.width // 2, self.y, -10)
            bullets.append(bullet)
            self.shoot_cooldown = 15  # Cooldown frames between shots

    def update(self):
        # Update cooldown timer
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, surface):
        # Draw player as a blue rectangle
        pygame.draw.rect(surface, self.color, self.rect)
        # Draw health bar above player
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = self.width
        bar_height = 6
        # Calculate health ratio
        health_ratio = self.health / self.max_health
        # Background bar (gray)
        pygame.draw.rect(surface, GRAY, (self.x, self.y - 10, bar_width, bar_height))
        # Health bar (green)
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 10, bar_width * health_ratio, bar_height))


class Bullet:
    """ Bullet class fired by the player """
    def __init__(self, x, y, speed_y):
        self.radius = 5
        self.x = x
        self.y = y
        self.speed_y = speed_y
        self.color = YELLOW
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.radius * 2, self.radius * 2)

    def update(self):
        # Move bullet vertically
        self.y += self.speed_y
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        # Draw bullet as a yellow circle
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


class Enemy:
    """ Enemy class that moves randomly or chases player """
    def __init__(self):
        self.width = 30
        self.height = 30
        # Spawn at random position on top half of screen
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.color = RED
        self.speed = 2
        self.health = 30
        self.max_health = 30
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = random.choice(['left', 'right', 'up', 'down', 'idle'])
        self.change_direction_counter = 0

    def move(self, player):
        # Simple AI to chase player or move randomly
        distance_x = player.x - self.x
        distance_y = player.y - self.y
        distance = math.hypot(distance_x, distance_y)

        # If player is close, chase player
        if distance < 200:
            # Normalize direction vector for chasing
            if distance != 0:
                norm_x = distance_x / distance
                norm_y = distance_y / distance
                self.x += norm_x * self.speed
                self.y += norm_y * self.speed
        else:
            # Random movement - change direction occasionally
            if self.change_direction_counter == 0:
                self.direction = random.choice(['left', 'right', 'up', 'down', 'idle'])
                self.change_direction_counter = random.randint(30, 60)

            if self.direction == 'left' and self.x - self.speed > 0:
                self.x -= self.speed
            elif self.direction == 'right' and self.x + self.speed + self.width < SCREEN_WIDTH:
                self.x += self.speed
            elif self.direction == 'up' and self.y - self.speed > 0:
                self.y -= self.speed
            elif self.direction == 'down' and self.y + self.speed + self.height < SCREEN_HEIGHT:
                self.y += self.speed

            self.change_direction_counter -= 1

        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        # Draw enemy as a red rectangle
        pygame.draw.rect(surface, self.color, self.rect)
        # Draw health bar above enemy
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = self.width
        bar_height = 5
        # Calculate health ratio
        health_ratio = self.health / self.max_health
        # Background bar (gray)
        pygame.draw.rect(surface, GRAY, (self.x, self.y - 8, bar_width, bar_height))
        # Health bar (green)
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 8, bar_width * health_ratio, bar_height))


def main():
    # Main game loop
    run = True
    player = Player()
    bullets = []
    enemies = []

    # Spawn initial enemies
    for _ in range(5):
        enemies.append(Enemy())

    font = pygame.font.SysFont(None, 48)
    game_over = False

    while run:
        clock.tick(FPS)  # Set FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Shooting bullets on space bar press
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    player.shoot(bullets)

        keys_pressed = pygame.key.get_pressed()
        if not game_over:
            player.handle_movement(keys_pressed)
            player.update()

            # Update bullets
            for bullet in bullets[:]:
                bullet.update()
                # Remove bullet if it goes off screen
                if bullet.y < 0:
                    bullets.remove(bullet)

            # Update enemies
            for enemy in enemies[:]:
                enemy.move(player)

            # Check bullet-enemy collisions
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.health -= 10  # Bullet damage
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                        break

            # Check enemy-player collisions (damage player)
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    # Reduce player health gradually
                    player.health -= 0.5
                    if player.health <= 0:
                        player.health = 0
                        game_over = True
                        break

        # Drawing
        screen.fill(BLACK)  # Clear screen

        if not game_over:
            # Draw player
            player.draw(screen)
            # Draw bullets
            for bullet in bullets:
                bullet.draw(screen)
            # Draw enemies
            for enemy in enemies:
                enemy.draw(screen)
        else:
            # Show Game Over text
            game_over_text = font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, text_rect)

        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

