import pygame
import pickle
import sys
from network import Network

pygame.font.init()


width = 700
height = 700
DISPLAYSURF = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rock - Scissor - Paper')


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100


    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self. width, self.height))
        font = pygame.font.SysFont('Montserrat', 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))


    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_win(win, game, player):
    win.fill((128, 128, 128))
    
    if not (game.connected()):
        font = pygame.font.SysFont('Montserrat', 60)
        text = font.render('Waiting for Player...', 1, (255, 0, 0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont('Montserrat', 60)
        text = font.render('Your move', 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render('Opponents', 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move_1 = game.get_player_move(0)
        move_2 = game.get_player_move(1)

        if game.both_moves():
            text_1 = font.render(move_1, 1, (0, 0, 0))
            text_2 = font.render(move_2, 1, (0, 0, 0))
        else:
            if game.p1_move and player == 0:
                text_1 = font.render(move_1, 1, (0, 0, 0))

            elif game.p1_move:
                text_1 = font.render('Locked in', 1, (0, 0, 0))
            
            else:
                text_1 = font.render('Waiting...', 1, (0, 0, 0))

            if game.p2_move and player == 1:
                text_2 = font.render(move_2, 1, (0, 0, 0))

            elif game.p2_move:
                text_2 = font.render('Locked in', 1, (0, 0, 0))
            
            else:
                text_2 = font.render('Waiting...', 1, (0, 0, 0))

        if player == 1:
            win.blit(text_2, (100, 350))
            win.blit(text_1, (400, 350))
        
        else:
            win.blit(text_1, (100, 350))
            win.blit(text_2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()






btns = [Button('Rock', 50, 500, (0, 0, 0)), Button('Scissors', 250, 500, (255, 0, 0)), Button('Paper', 450, 500, (0, 255, 0))]


def main():
    
    clock = pygame.time.Clock()
    network_1 = Network()
    player = int(network_1.get_player())
    print("You're the player ", player)

    while True:
        clock.tick(60)

        try:
            game = network_1.send('get')
        except:
            print("Couldn't get the game")
            break

        if game.both_moves():
            redraw_win(DISPLAYSURF, game, player)
            pygame.time.delay(200)
            try:
                game = network_1.send('reset')
            except:
                print("Couldn't get game")
                break

            
            font = pygame.font.SysFont('Montserrat', 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render('You won!!', 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render('Tie game', 1, (255, 0, 0))
            else:
                text = font.render('You lost..', 1, (255, 0, 0))

            DISPLAYSURF.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1_move:
                                network_1.send(btn.text)

                        else:
                            if not game.p2_move:
                                network_1.send(btn.text)

        redraw_win(DISPLAYSURF, game, player)

def menu_screen():
    run =  True
    clock = pygame.time.Clock()


    while run:
        clock.tick(60)
        DISPLAYSURF.fill((128, 128, 128))
        font = pygame.font.SysFont('Montserrat', 60)
        text = font.render('Click to play', 1, (255, 0, 0))
        DISPLAYSURF.blit(text, (300, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                run = False

    main()




if __name__ == "__main__":
    while True:
        menu_screen()

