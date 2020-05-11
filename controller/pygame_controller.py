import pygame
import time
import controller
import notemap

ctrl = controller.Controller("cloud.itsw.es")

pygame.init()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Vibrance Control")
clock = pygame.time.Clock()

color = notemap.PALETTE[0]

running = True

enabled = {port:False for port in range(9001, 9007)}

updateNeeded = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (ord('0') <= event.key <= ord('9')) or (pygame.K_KP0 <= event.key <= pygame.K_KP9):
                if event.key in (pygame.K_KP1, ord('1')):
                    enabled[9001] = True
                    enabled[9004] = True
                elif event.key in (pygame.K_KP2, ord('2')):
                    enabled[9002] = True
                    enabled[9005] = True
                elif event.key in (pygame.K_KP3, ord('3')):
                    enabled[9003] = True
                    enabled[9006] = True
                elif event.key in (pygame.K_KP4, ord('4')):
                    enabled[9004] = True
                elif event.key in (pygame.K_KP5, ord('5')):
                    enabled[9005] = True
                elif event.key in (pygame.K_KP6, ord('6')):
                    enabled[9006] = True
                elif event.key in (pygame.K_KP7, ord('7')):
                    enabled[9001] = True
                elif event.key in (pygame.K_KP8, ord('8')):
                    enabled[9002] = True
                elif event.key in (pygame.K_KP9, ord('9')):
                    enabled[9003] = True
                elif event.key in (pygame.K_KP0, ord('0')):
                    enabled[9001] = True
                    enabled[9002] = True
                    enabled[9003] = True
                    enabled[9004] = True
                    enabled[9005] = True
                    enabled[9006] = True
            else:
                if event.key == ord('q'):
                    color = notemap.PALETTE[0]
                elif event.key == ord('w'):
                    color = notemap.PALETTE[1]
                elif event.key == ord('e'):
                    color = notemap.PALETTE[2]
                elif event.key == ord('r'):
                    color = notemap.PALETTE[3]
                elif event.key == ord('a'):
                    color = notemap.PALETTE[4]
                elif event.key == ord('s'):
                    color = notemap.PALETTE[5]
                elif event.key == ord('d'):
                    color = notemap.PALETTE[6]
                elif event.key == ord('f'):
                    color = notemap.PALETTE[7]
                elif event.key == ord('z'):
                    color = notemap.PALETTE[8]
                elif event.key == ord('x'):
                    color = notemap.PALETTE[9]
                elif event.key == ord('c'):
                    color = notemap.PALETTE[10]
                elif event.key == ord('v'):
                    color = notemap.PALETTE[11]
            updateNeeded = True

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_KP1, ord('1')):
                enabled[9001] = False
                enabled[9004] = False
            elif event.key in (pygame.K_KP2, ord('2')):
                enabled[9002] = False
                enabled[9005] = False
            elif event.key in (pygame.K_KP3, ord('3')):
                enabled[9003] = False
                enabled[9006] = False
            elif event.key in (pygame.K_KP4, ord('4')):
                enabled[9004] = False
            elif event.key in (pygame.K_KP5, ord('5')):
                enabled[9005] = False
            elif event.key in (pygame.K_KP6, ord('6')):
                enabled[9006] = False
            elif event.key in (pygame.K_KP7, ord('7')):
                enabled[9001] = False
            elif event.key in (pygame.K_KP8, ord('8')):
                enabled[9002] = False
            elif event.key in (pygame.K_KP9, ord('9')):
                enabled[9003] = False
            elif event.key in (pygame.K_KP0, ord('0')):
                enabled[9001] = False
                enabled[9002] = False
                enabled[9003] = False
                enabled[9004] = False
                enabled[9005] = False
                enabled[9006] = False
            updateNeeded = True

    if updateNeeded:
        ctrl.clear()
        for port in enabled.keys():
            ctrl.add(port, color if enabled[port] else "000")
        ctrl.write()
        updateNeeded = False

    pygame.draw.rect(screen, pygame.Color("#"+color), (0, 0, 1000, 500))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
