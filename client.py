'''
Client server
'''
import pygame
import sys
from network import Network


width = 500
height = 500


DISPLAYSURF = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

client_number = 0

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
    

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)


    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel
        
        self.update()


    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def redraw_win(win, player1, player2):

    DISPLAYSURF.fill((255, 255, 255))
    player1.draw(win)
    player2.draw(win)
    pygame.display.update()



def read_pos(str1):
    str_list = str1.split(',')
    print('read pos',str1)
    return int(str_list[0]), int(str_list[1])



def make_pos(tup1):
    print('Esta es la tupla', tup1)
    return str(tup1[0]) + ',' + str(tup1[1])


def main():

    network_1 = Network()
    start_pos = read_pos(network_1.get_pos())
    print()

    player_1 = Player(start_pos[0], start_pos[1], 100, 100, (0, 255, 0))
    player_2 = Player(0, 0, 100, 100, (255, 0, 0))


    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        player_2_pos = read_pos(network_1.send(make_pos((player_1.x, player_1.y))))
        player_2.x = player_2_pos[0]
        player_2.y = player_2_pos[1]
        player_2.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                

        player_1.move()
        redraw_win(DISPLAYSURF, player_1, player_2)


if __name__ == "__main__":
    main()