
class Game:
    def __init__(self, id):
        self.p1_move = False
        self.p2_move = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, player):
        '''
        :param player: [0,1]
        :return: Move
        '''

        return self.moves[player]


    def play(self, player, move):

        self.moves[player] = move

        if player == 0:
            self.p1_move = True
        else:
            self.p2_move = True

    
    def connected(self):
        return self.ready


    def both_moves(self):
        return self.p1_move and self.p2_move

    
    def winner(self):
        player_1 = self.moves[0].upper()[0]
        player_2 = self.moves[1].upper()[0]

        winner = -1

        if player_1 == 'R' and player_2 == 'S':
            winner = 0

        elif player_1 == 'S' and player_2 == 'R':
            winner = 1

        elif player_1 == 'P' and player_2 == 'R':
            winner = 0

        elif player_1 == 'R' and player_2 == 'P':
            winner = 1

        elif player_1 == 'S' and player_2 == 'P':
            winner = 0

        elif player_1 == 'P' and player_2 == 'S':
            winner = 1

        return winner


    def reset_moves(self):
        self.p1_move = False
        self.p2_move = False







