import pygame
import time
import controller

ctrl = controller.Controller()

pygame.init()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Vibrance Control")
clock = pygame.time.Clock()

color = "0F0"

running = True

frame = 0;

changes = {}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_KP1, ord('1')):
                changes[9001] = color
                changes[9004] = color
            elif event.key in (pygame.K_KP2, ord('2')):
                changes[9002] = color
                changes[9005] = color
            elif event.key in (pygame.K_KP3, ord('3')):
                changes[9003] = color
                changes[9006] = color
            elif event.key in (pygame.K_KP4, ord('4')):
                changes[9004] = color
            elif event.key in (pygame.K_KP5, ord('5')):
                changes[9005] = color
            elif event.key in (pygame.K_KP6, ord('6')):
                changes[9006] = color
            elif event.key in (pygame.K_KP7, ord('7')):
                changes[9001] = color
            elif event.key in (pygame.K_KP8, ord('8')):
                changes[9002] = color
            elif event.key in (pygame.K_KP9, ord('9')):
                changes[9003] = color
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_KP1, ord('1')):
                changes[9001] = "000"
                changes[9004] = "000"
            elif event.key in (pygame.K_KP2, ord('2')):
                changes[9002] = "000"
                changes[9005] = "000"
            elif event.key in (pygame.K_KP3, ord('3')):
                changes[9003] = "000"
                changes[9006] = "000"
            elif event.key in (pygame.K_KP4, ord('4')):
                changes[9004] = "000"
            elif event.key in (pygame.K_KP5, ord('5')):
                changes[9005] = "000"
            elif event.key in (pygame.K_KP6, ord('6')):
                changes[9006] = "000"
            elif event.key in (pygame.K_KP7, ord('7')):
                changes[9001] = "000"
            elif event.key in (pygame.K_KP8, ord('8')):
                changes[9002] = "000"
            elif event.key in (pygame.K_KP9, ord('9')):
                changes[9003] = "000"

    if frame % 3 == 0:
        for port in changes.keys():
            ctrl.setColor(port, changes[port])
        changes = {}
        ctrl.write()
    pygame.display.flip()
    frame += 1
    clock.tick(30)

pygame.quit()
