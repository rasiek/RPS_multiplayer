'''
Client server
'''
import pygame
import sys
from network import Network
from player import Player


width = 500
height = 500


DISPLAYSURF = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')



def redraw_win(win, player1, player2):

    DISPLAYSURF.fill((255, 255, 255))
    player1.draw(win)
    player2.draw(win)
    pygame.display.update()



def main():

    network_1 = Network()

    player_1 = network_1.get_player()

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        player_2 = network_1.send(player_1)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                

        player_1.move()
        redraw_win(DISPLAYSURF, player_1, player_2)


if __name__ == "__main__":
    main()