import pygame
import time
import controller

ctrl = controller.Controller("cloud.itsw.es")

pygame.init()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Vibrance Control")
clock = pygame.time.Clock()

color = "0F0"

running = True

colors = {port:"000" for port in range(9001, 9007)}

updateNeeded = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_KP1, ord('1')):
                colors[9001] = color
                colors[9004] = color
            elif event.key in (pygame.K_KP2, ord('2')):
                colors[9002] = color
                colors[9005] = color
            elif event.key in (pygame.K_KP3, ord('3')):
                colors[9003] = color
                colors[9006] = color
            elif event.key in (pygame.K_KP4, ord('4')):
                colors[9004] = color
            elif event.key in (pygame.K_KP5, ord('5')):
                colors[9005] = color
            elif event.key in (pygame.K_KP6, ord('6')):
                colors[9006] = color
            elif event.key in (pygame.K_KP7, ord('7')):
                colors[9001] = color
            elif event.key in (pygame.K_KP8, ord('8')):
                colors[9002] = color
            elif event.key in (pygame.K_KP9, ord('9')):
                colors[9003] = color
            elif event.key in (pygame.K_KP0, ord('0')):
                colors[9001] = color
                colors[9002] = color
                colors[9003] = color
                colors[9004] = color
                colors[9005] = color
                colors[9006] = color
            updateNeeded = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_KP1, ord('1')):
                colors[9001] = "000"
                colors[9004] = "000"
            elif event.key in (pygame.K_KP2, ord('2')):
                colors[9002] = "000"
                colors[9005] = "000"
            elif event.key in (pygame.K_KP3, ord('3')):
                colors[9003] = "000"
                colors[9006] = "000"
            elif event.key in (pygame.K_KP4, ord('4')):
                colors[9004] = "000"
            elif event.key in (pygame.K_KP5, ord('5')):
                colors[9005] = "000"
            elif event.key in (pygame.K_KP6, ord('6')):
                colors[9006] = "000"
            elif event.key in (pygame.K_KP7, ord('7')):
                colors[9001] = "000"
            elif event.key in (pygame.K_KP8, ord('8')):
                colors[9002] = "000"
            elif event.key in (pygame.K_KP9, ord('9')):
                colors[9003] = "000"
            elif event.key in (pygame.K_KP0, ord('0')):
                colors[9001] = "000"
                colors[9002] = "000"
                colors[9003] = "000"
                colors[9004] = "000"
                colors[9005] = "000"
                colors[9006] = "000"
            updateNeeded = True

    if updateNeeded:
        for port in colors.keys():
            ctrl.setColor(port, colors[port])
        ctrl.write()
        updateNeeded = False
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
