import random
from enum import Enum


class Bcolors:
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
    P1 = Token('P1', Bcolors.RED)
    P2 = Token('P2', Bcolors.YELLOW)


class Player:
    def __init__(self, name: str, tag: str, token=Tokens.P1.value) -> None:
        self.name = name
        self.tag = tag
        self.token = token

    def get_token(self):
        return self.token

    def get_username(self):
        return self.name

    def get_tag(self):
        return self.tag


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
                    result += f'║{tile.get_color()}{BoardTile.TOKEN.value}{Bcolors.ENDC}'
                elif tile is None:
                    result += '║' + BoardTile.EMPTY.value
            result += '║\n'

        result += '╚══' + '══' * (self.width - 2) + '═╝\n'
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
            tile = self.board[current_row][current_col]
            if tile is not None and tile.get_color() == token_color:
                count += 1
            else:
                count = 0
            if current_row == end[0] and current_col == end[1]:
                break
            current_row += row_offset
            current_col += col_offset

        return count == conn_length


class ConsoleRenderer:
    def __init__(self, game_board) -> None:
        self.game_board = game_board

    def render_board(self) -> None:
        print(self.game_board)

    @classmethod
    def render_title_box(cls, sentence) -> None:
        print(sentence)

    @classmethod
    def render_text_box(cls, sentence) -> None:
        pass

    @classmethod
    def render_text(cls, text) -> None:
        print(text)


class ConnectFour:
    def __init__(self, renderer: ConsoleRenderer, game_board, players: list[Player]) -> None:
        self.renderer = renderer
        self.players = players
        self.game_board = game_board
        self.player_count = len(self.players)

    def run(self) -> None:
        self.renderer.render_title_box('Welcome to Connect Four!!!')

        continue_running = True
        current_player = self.players[random.randint(0, self.player_count - 1)]
        self.renderer.render_board()
        self.renderer.render_text(f'{current_player.get_tag()} ({current_player.get_username()}) starts the game.')
        while continue_running:
            selected_lane = int(input(f'{current_player.get_tag()} ({current_player.get_username()}) places token in lane: '))
            row, col = self.game_board.place_token(current_player, selected_lane)
            did_win = self.game_board.check_win_conditon(row, col, 4)
            self.renderer.render_board()

            # For debugging purposes
            continue_running = False


class ConnectFour2PFactory:
    def __init__(self) -> None:
        self.rules = {'username': {'length': {'min': 3, max: 20}}}

    @staticmethod
    def build() -> ConnectFour:
        game_board = Board(7, 6)
        player_name_prompt = '{player} enter your name: '
        player1_name = input(player_name_prompt.format(player="Player 1"))
        player2_name = input(player_name_prompt.format(player="Player 2"))

        player1 = Player(player1_name, 'Player 1', Tokens.P1.value)
        player2 = Player(player2_name, 'Player 2', Tokens.P2.value)

        return ConnectFour(
            renderer=ConsoleRenderer(game_board),
            game_board=game_board,
            players=[player1, player2]
        )

    def __get_username(self, tag):
        player_name_prompt = '{tag} enter your name: '
        keep_trying = True
        while keep_trying:
            try:
                player_name = input(player_name_prompt.format(tag=tag))
                keep_trying = not self.__validate_username(player_name)
                return player_name
            except Exception as e:
                print(str(e))

    def __validate_username(self, username: str) -> bool:
        if username is None:
            raise Exception('Invalid username.')

        username_len = len(username)
        if username_len == 0:
            raise Exception('C\'mon... Please enter someting.')

        if username_len < self.rules['username']['length']['min']:
            raise Exception('Username too short.')

        if username_len > self.rules['username']['length']['max']:
            raise Exception('Username too long.')

        return True


if __name__ == '__main__':
    game = ConnectFour2PFactory.build()
    game.run()
