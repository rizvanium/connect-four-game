from os import system, name
from domain.game_board import Board, BoardTile
from domain.colors import Bcolors


class ConsoleRenderer:
    def __init__(self, game_board: Board) -> None:
        self.game_board = game_board

    def render_board(self, game_ended: bool, connected_tiles: list[tuple[int, int]]) -> None:
        result = '╔══' + '══' * (self.game_board.width - 2) + '═╗\n'

        for row_idx, row in enumerate(self.game_board.board):
            for col_idx, tile in enumerate(row):
                if tile is None:
                    result += '║' + BoardTile.EMPTY.value
                elif game_ended and (row_idx, col_idx) in connected_tiles:
                    result += f'║{tile.get_color()}{BoardTile.CONNECTED.value}{Bcolors.ENDC}'
                else:
                    result += f'║{tile.get_color()}{BoardTile.TOKEN.value}{Bcolors.ENDC}'
            result += '║\n'

        result += '╚══' + '══' * (self.game_board.width - 2) + '═╝\n'
        header_numbers = ' '.join(str(x) for x in range(1, self.game_board.width + 1))
        result += ' ' + header_numbers + ' '

        self.__clear()
        print(result)

    @classmethod
    def render_title_box(cls, sentence) -> None:
        print(sentence)

    @classmethod
    def render_text_box(cls, sentence) -> None:
        pass

    @classmethod
    def render_text(cls, text) -> None:
        print(text)

    @staticmethod
    def __clear() -> None:
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
