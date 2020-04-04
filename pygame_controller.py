import pygame

import controller

ctrl = controller.Controller()

pygame.init()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Vibrance Control")
clock = pygame.time.Clock()

color = "0F0"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_KP1, ord('1')):
                ctrl.setColor(9001, color)
                ctrl.setColor(9004, color)
            elif event.key in (pygame.K_KP2, ord('2')):
                ctrl.setColor(9002, color)
                ctrl.setColor(9005, color)
            elif event.key in (pygame.K_KP3, ord('3')):
                ctrl.setColor(9003, color)
                ctrl.setColor(9006, color)
            elif event.key in (pygame.K_KP4, ord('4')):
                ctrl.setColor(9004, color)
            elif event.key in (pygame.K_KP5, ord('5')):
                ctrl.setColor(9005, color)
            elif event.key in (pygame.K_KP6, ord('6')):
                ctrl.setColor(9006, color)
            elif event.key in (pygame.K_KP7, ord('7')):
                ctrl.setColor(9001, color)
            elif event.key in (pygame.K_KP8, ord('8')):
                ctrl.setColor(9002, color)
            elif event.key in (pygame.K_KP9, ord('9')):
                ctrl.setColor(9003, color)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_KP1, ord('1')):
                ctrl.setColor(9001, "000")
                ctrl.setColor(9004, "000")
            elif event.key in (pygame.K_KP2, ord('2')):
                ctrl.setColor(9002, "000")
                ctrl.setColor(9005, "000")
            elif event.key in (pygame.K_KP3, ord('3')):
                ctrl.setColor(9003, "000")
                ctrl.setColor(9006, "000")
            elif event.key in (pygame.K_KP4, ord('4')):
                ctrl.setColor(9004, "000")
            elif event.key in (pygame.K_KP5, ord('5')):
                ctrl.setColor(9005, "000")
            elif event.key in (pygame.K_KP6, ord('6')):
                ctrl.setColor(9006, "000")
            elif event.key in (pygame.K_KP7, ord('7')):
                ctrl.setColor(9001, "000")
            elif event.key in (pygame.K_KP8, ord('8')):
                ctrl.setColor(9002, "000")
            elif event.key in (pygame.K_KP9, ord('9')):
                ctrl.setColor(9003, "000")

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
