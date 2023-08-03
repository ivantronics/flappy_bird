import pygame
import os

from bird import Bird
from pipe import Pipe
from ground import Ground
from image_scaler import image_scaler

pygame.font.init()

WIN_WIDTH = 576
WIN_HEIGHT = 800

SCORE_FONT = pygame.font.SysFont('calibri', 50, bold=True)
BG_IMG = image_scaler(os.path.join("images", "bg.png"))


def draw_window(window, bird, pipes, ground, score):
    window.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    score_text = SCORE_FONT.render(f"Score = {score[0]}", 1, (255, 255, 255))
    window.blit(score_text, (WIN_WIDTH - 10 - score_text.get_width(), 10))
    ground.draw(window)
    bird.draw(window)
    pygame.display.update()


def pipe_logic(window, pipes, bird, score):
    new_pipe = False  # Point of adding new pipe
    pipes_to_remove = []  # List of pipes to remove from the pipes list
    for pipe in pipes:
        if pipe.collision(bird):
            end_screen(window)
        if not pipe.passed and pipe.x + pipe.PIPE_WIDTH < bird.x:
            pipe.passed = True
            new_pipe = True
        if pipe.x + pipe.PIPE_WIDTH < 0:
            pipes_to_remove.append(pipe)

        pipe.move()

    if new_pipe:
        score[0] += 1
        pipes.append(Pipe(600))

    for pipe_to_remove in pipes_to_remove:
        pipes.remove(pipe_to_remove)


def end_screen(window):
    run = True
    text_label = SCORE_FONT.render("Press Space to Restart",
                                   True,
                                   (255, 255, 255))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()

        window.blit(text_label,
                    (WIN_WIDTH / 2 - text_label.get_width() / 2, 500))
        pygame.display.update()

    pygame.quit()
    quit()


def main():
    clock = pygame.time.Clock()
    bird = Bird(230, 350)
    birds = []
    ground = Ground(730)
    pipes = [Pipe(600)]

    score = [0]

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True

    while run:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_SPACE:
                bird.jump()

        bird.move()
        ground.move()
        pipe_logic(window, pipes, bird, score)
        draw_window(window, bird, pipes, ground, score)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
