from enum import Enum

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\u001b[31m'
    YELLOW = '\u001b[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Token:
    def __init__(self, name, color_val):
        self.name = name
        self.color = color_val
    
    def get_name(self):
        return self.name

    def get_color(self):
        return self.color


class Tokens(Enum):
    P1 = Token('P1', bcolors.RED)
    P2 = Token('P2', bcolors.YELLOW)


class Player:
    def __init__(self, name, token = Tokens.P1) -> None:
        self.name = name
        self.token = token

    def get_token(self):
        return self.token

    def get_username(self):
        return self.name


class BoardTile(Enum):
    EMPTY = '●'
    TOKEN = '●'
    CONNECTED = '◉'


class Board:
    def __init__(self, width = 0, length = 0) -> None:
        self.width = width
        self.length = length
        self.board = [[None] * width for _ in range(length)]
    

    def __repr__(self):

        result = '╔══' + '══' * (self.width - 2) + '═╗\n'

        for row in self.board:
            for tile in row:
                if isinstance(tile, Token):
                    result += f'║{tile.get_color()}{BoardTile.TOKEN.value}{bcolors.ENDC}'
                elif tile == None:
                    result += '║' + BoardTile.EMPTY.value
            result += '║\n'

        result += '╚══' + '══'* (self.width - 2) + '═╝\n'
        header_numbers = ' '.join(str(x) for x in range(1, self.width + 1))
        result += ' ' + header_numbers + ' '

        return result
    

    def place_token(self, player, lane) -> None:
        col = lane - 1
        if col < 0 or col > self.width - 1:
            raise Exception(f'Select an existing lane.')

        for idx in reversed(range(self.length)):
            if self.board[idx][col] == None:
                self.board[idx][col] = player.get_token()
                return
        
        raise Exception(f'{lane} lane is filled, try other lane.')


class ConnectFour:
    def __init__(self, renderer) -> None:
        self.renderer = renderer
    
    def run(self) -> None:
        print('Game is running!!!')


class LetterSize(Enum):
    SMALL = 0,
    MEDIUM = 1,
    LARGE = 2


class ConsoleRenderer:
    def __init__(self, game_board) -> None:
        self.game_board = game_board
    

    def render_board(self) -> None:
        print(self.game_board)


    def render_title_box(sentence) -> None:
        ConsoleRenderer.draw_sentence(sentence, size = LetterSize.LARGE)


    def render_text_box(sentence) -> None:
        pass



if __name__ == '__main__':
    game = ConnectFour(None)
    game.run()
    board = Board(7, 6)

    player1 = Player('P1', Tokens.P1.value)
    player2 = Player('P2', Tokens.P2.value)

    board.place_token(player1, 1)
    board.place_token(player2, 1)
    board.place_token(player1, 7)
    print(board)