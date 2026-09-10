import pygame
import random
import sys


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

GRAVITY = 0.5
JUMP_VELOCITY = -10
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_VELOCITY = -4
PIPE_SPAWN_INTERVAL = 1500

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.radius = 15
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.centery = self.y

    def jump(self):
        self.velocity = JUMP_VELOCITY

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x) + 5, int(self.y) - 5), 3)

        font = pygame.font.SysFont("Arial", 24)
        beak = font.render("<", True, RED)

        screen.blit(beak, (int(self.x) + self.radius - 2, int(self.y) - 14))

    def get_rect(self):
        return self.rect


class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        self.top_height = random.randint(100, SCREEN_HEIGHT - self.gap - 100)
        self.bottom_y = self.top_height + self.gap
        self.passed = False

        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y)

    def update(self):
        self.x += PIPE_VELOCITY
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def off_screen(self):
        return self.x + self.width < 0

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

    def collide(self, bird_rect):
        return self.top_rect.colliderect(bird_rect) or self.bottom_rect.colliderect(bird_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 50)

        self.reset()

    def reset(self):
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.start_screen = True
        self.last_pipe_spawn = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.start_screen:
                        self.start_screen = False
                    elif not self.game_over:
                        self.bird.jump()
                    else:
                        self.reset()

    def update(self):
        if self.start_screen or self.game_over:
            return

        self.bird.update()

        if self.bird.y - self.bird.radius <= 0 or self.bird.y + self.bird.radius >= SCREEN_HEIGHT:
            self.game_over = True

        now = pygame.time.get_ticks()

        if now - self.last_pipe_spawn > PIPE_SPAWN_INTERVAL:
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.last_pipe_spawn = now

        for pipe in self.pipes[:]:
            pipe.update()

            if pipe.collide(self.bird.get_rect()):
                self.game_over = True

            if pipe.off_screen():
                self.pipes.remove(pipe)

            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1

    def draw(self):
        self.screen.fill(BLUE)

        self.bird.draw(self.screen)

        for pipe in self.pipes:
            pipe.draw(self.screen)

        score_text = self.font.render(f"Счёт: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.start_screen:
            self.draw_start_screen()

        if self.game_over:
            self.draw_game_over_screen()

        pygame.display.flip()

    def draw_start_screen(self):
        title = self.big_font.render("Flappy Bird", True, WHITE)
        instruction = self.font.render("Нажмите ПРОБЕЛ для старта", True, WHITE)

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        self.screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 300))

    def draw_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.big_font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Ваш счёт: {self.score}", True, WHITE)
        restart_text = self.font.render("Нажмите ПРОБЕЛ для рестарта", True, WHITE)

        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()