from enum import Enum
from domain.player import Player


class BoardTile(Enum):
    EMPTY = '●'
    TOKEN = '●'
    CONNECTED = '◎'


class Board:
    def __init__(self, width=0, length=0) -> None:
        self.width = width
        self.length = length
        self.board = [[None] * width for _ in range(length)]
        self.token_positions = {}

    def place_token(self, player: Player, lane: int) -> tuple[int, int]:
        col = lane - 1
        if col < 0 or col > self.width - 1:
            raise Exception(f'Select an existing lane.')

        for idx in reversed(range(self.length)):
            if self.board[idx][col] is None:
                self.board[idx][col] = player.get_token()
                return idx, col,

        raise Exception(f'{lane} lane is filled, try other lane.')

    def check_win_conditon(self, row: int, col: int, conn_length: int) -> tuple[bool, list[tuple[int, int]]]:
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
        top_right = (row - offset_top_right, col + offset_top_right)

        game_has_ended, connected_tiles = self.contains_same_color_tokens(token_color, left, right, conn_length)
        if game_has_ended:
            return game_has_ended, connected_tiles

        game_has_ended, connected_tiles = self.contains_same_color_tokens(token_color, top, bottom, conn_length)
        if game_has_ended:
            return game_has_ended, connected_tiles

        game_has_ended, connected_tiles = self.contains_same_color_tokens(token_color, bottom_left, top_right,
                                                                          conn_length)
        if game_has_ended:
            return game_has_ended, connected_tiles

        game_has_ended, connected_tiles = self.contains_same_color_tokens(token_color, top_left, bottom_right,
                                                                          conn_length)
        if game_has_ended:
            return game_has_ended, connected_tiles

        return False, []

    def contains_same_color_tokens(self, token_color, start, end, conn_length) -> tuple[bool, list[tuple[int, int]]]:
        row_diff = start[0] - end[0]
        col_diff = start[1] - end[1]

        row_offset = 0 if row_diff == 0 else 1 if row_diff < 0 else - 1
        col_offset = 0 if col_diff == 0 else 1 if col_diff < 0 else - 1
        count = 0
        current_row, current_col = start[0], start[1]
        conencted_tiles = []
        while True:
            tile = self.board[current_row][current_col]
            if tile is not None and tile.get_color() == token_color:
                count += 1
                conencted_tiles.append((current_row, current_col))
            else:
                conencted_tiles.clear()
                count = 0

            if count == conn_length:
                return True, conencted_tiles

            if current_row == end[0] and current_col == end[1]:
                break

            current_row += row_offset
            current_col += col_offset

        return False, conencted_tiles

    def is_lane_filled(self, col):
        return self.board[0][col] is not None
