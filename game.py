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
    def __init__(self, name, token = Tokens.P1.value) -> None:
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
    def __init__(self, width=0, length=0) -> None:
        self.width = width
        self.length = length
        self.board = [[None] * width for _ in range(length)]
        self.token_positions = {}
    
    def __repr__(self):
        result = '╔══' + '══' * (self.width - 2) + '═╗\n'

        for row in self.board:
            for tile in row:
                if isinstance(tile, Token):
                    result += f'║{tile.get_color()}{BoardTile.TOKEN.value}{bcolors.ENDC}'
                elif tile is None:
                    result += '║' + BoardTile.EMPTY.value
            result += '║\n'

        result += '╚══' + '══'* (self.width - 2) + '═╝\n'
        header_numbers = ' '.join(str(x) for x in range(1, self.width + 1))
        result += ' ' + header_numbers + ' '

        return result
    
    def place_token(self, player: Player, lane: int) -> tuple[int, int]:
        col = lane - 1
        if col < 0 or col > self.width - 1:
            raise Exception(f'Select an existing lane.')

        for idx in reversed(range(self.length)):
            if self.board[idx][col] is None:
                self.board[idx][col] = player.get_token()
                return idx, col,
        
        raise Exception(f'{lane} lane is filled, try other lane.')

    def check_win_conditon(self, row: int, col: int, conn_length: int) -> bool:
        token = self.board[row][col]
        if token is None:
            return False

        token_color = token.get_color()

        left = (row, max(col - conn_length + 1, 0))
        right = (row, min(col + conn_length - 1, self.width - 1))
        top = (max(row - conn_length + 1, 0), col)
        bottom = (min(row + conn_length - 1, self.length - 1), col)

        dist_to_right = right[1] - col
        dist_to_left = col - left[1]
        dist_to_top = row - top[0]
        dist_to_bottom = bottom[0] - row

        offset_top_left = min(dist_to_left, dist_to_top)
        offset_top_right = min(dist_to_right, dist_to_top)
        offset_bottom_left = min(dist_to_left, dist_to_bottom)
        offset_bottom_right = min(dist_to_right, dist_to_bottom)

        bottom_left = (row + offset_bottom_left, col - offset_bottom_left)
        bottom_right = (row + offset_bottom_right, col + offset_bottom_right)
        top_left = (row - offset_top_left, col - offset_top_left)
        top_right = (row - offset_top_right, col + offset_bottom_right)

        if self.contains_same_color_tokens(token_color, left, right, conn_length):
            return True

        if self.contains_same_color_tokens(token_color, top, bottom, conn_length):
            return True

        if self.contains_same_color_tokens(token_color, bottom_left, top_right, conn_length):
            return True

        return self.contains_same_color_tokens(token_color, top_left, bottom_right, conn_length)

    def contains_same_color_tokens(self, token_color, start, end, conn_length):
        row_diff = start[0] - end[0]
        col_diff = start[1] - end[1]

        row_offset = 0 if row_diff == 0 else 1 if row_diff < 0 else - 1
        col_offset = 0 if col_diff == 0 else 1 if col_diff < 0 else - 1
        count = 0
        current_row, current_col = start[0], start[1]
        while True:
            print(f'current: {current_row}, {current_col}')
            tile = self.board[current_row][current_col]
            if tile is not None and tile.get_color() == token_color:
                count += 1
            else:
                count = 0
            if current_row == end[0] and current_col == end[1]:
                break
            current_row += row_offset
            current_col += col_offset
        print('-'*20)
        return count == conn_length


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
    board.place_token(player2, 6)
    row, col = board.place_token(player1, 6)

    print(board)
    print(f'row: {row} col: {col}')
    board.check_win_conditon(row, col, 4)