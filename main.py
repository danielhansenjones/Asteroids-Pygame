from asteroid import Asteroid
from constants import *
import pygame
from player import Player
from shot import Shot
from asteroidField import AsteroidField

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.time.Clock()


def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    last_shot_time = 0

    black = (0, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks() / 1000

        if keys[pygame.K_SPACE] and current_time - last_shot_time > PLAYER_SHOOT_COOLDOWN:
            last_shot_time = current_time
            shot = Shot(player.position.x, player.position.y)
            forward = pygame.Vector2(0, 1).rotate(player.rotation)
            shot.velocity = forward * PLAYER_SHOOT_SPEED

        updatable.update(dt)

        for asteroid in asteroids:
            dx = player.position.x - asteroid.position.x
            dy = player.position.y - asteroid.position.y
            distance = (dx * dx + dy * dy) ** 0.5
            if distance < (player.radius + asteroid.radius):
                print("Game Over!")
                return

        for shot in shots:
            for asteroid in asteroids:
                dx = shot.position.x - asteroid.position.x
                dy = shot.position.y - asteroid.position.y
                distance = (dx * dx + dy * dy) ** 0.5
                if distance < (shot.radius + asteroid.radius):
                    asteroid.split()
                    shot.kill()
                    break

            if (shot.position.x < -SHOT_RADIUS or
                    shot.position.x > SCREEN_WIDTH + SHOT_RADIUS or
                    shot.position.y < -SHOT_RADIUS or
                    shot.position.y > SCREEN_HEIGHT + SHOT_RADIUS):
                shot.kill()

        screen.fill(black)
        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == '__main__':
    main()