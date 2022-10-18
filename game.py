import random
from domain.game_board import Board
from domain.player import Player
from domain.token import Tokens
from services.renderers import ConsoleRenderer


class ConnectFour:
    def __init__(self, renderer: ConsoleRenderer, game_board: Board, players: list[Player]) -> None:
        self.renderer = renderer
        self.players = players
        self.game_board = game_board
        self.player_count = len(self.players)
        self.rules = {'lane': {'min': 1, 'max': game_board.width}}

    def run(self) -> None:
        self.renderer.render_title_box('Welcome to Connect Four!!!')

        player_idx = random.randint(0, self.player_count - 1)
        current_player = self.players[player_idx]
        self.renderer.render_board(game_ended=False, connected_tiles=[])
        self.renderer.render_text(f'{current_player.get_tag()} ({current_player.get_username()}) starts the game.')

        continue_running = True
        while continue_running:
            selected_lane = self.__get_lane(current_player)
            row, col = self.game_board.place_token(current_player, selected_lane)
            game_ended, connected_tiles = self.game_board.check_win_conditon(row, col, 4)
            self.renderer.render_board(game_ended, connected_tiles)
            if game_ended:
                self.renderer.render_text(
                    f'{current_player.get_tag()} ({current_player.get_username()}) has won the game!!!')
                continue_running = False
            else:
                player_idx = (player_idx + 1) % self.player_count
                current_player = self.players[player_idx]

    def __get_lane(self, current_player: Player) -> int:
        tag, username = current_player.get_tag(), current_player.get_username()
        prompt = f'{tag} ({username}) tries placing token in lane: '

        keep_trying = True
        while keep_trying:
            lane = input(prompt)
            is_valid, msg = self.__validate_lane_input(lane)
            keep_trying = not is_valid
            if not keep_trying:
                return int(lane)
            prompt = msg

    def __validate_lane_input(self, lane_input: str) -> tuple[bool, str]:
        try:
            int(lane_input)
        except ValueError:
            return False, 'But fails, because poor {username} doesn\'t know that he needs to enter a lane ' \
                          'number.\nAnd so again, he again tries placing a token in a lane: '

        lane_num = int(lane_input)
        if lane_num < self.rules['lane']['min'] or lane_num > self.rules['lane']['max']:
            return False, 'But fails to do so, because he\'s trolling and entering non existent lane number.\n' \
                          'And so again, he tries placing a token in a lane: '

        if self.game_board.is_lane_filled(lane_num - 1):
            return False, 'But fails to do so, because the lane is filled to the top.\n' \
                          'And so again, he tries placing a token in a lane: '

        return True, ''


class ConnectFour2PFactory:
    rules = {'username': {'length': {'min': 3, 'max': 20}}}

    @classmethod
    def build(cls) -> ConnectFour:
        game_board = Board(7, 6)

        player1_name = cls.__get_username('Player 1')
        player2_name = cls.__get_username('Player 2')

        player1 = Player(player1_name, 'Player 1', Tokens.P1.value)
        player2 = Player(player2_name, 'Player 2', Tokens.P2.value)

        return ConnectFour(
            renderer=ConsoleRenderer(game_board),
            game_board=game_board,
            players=[player1, player2]
        )

    @classmethod
    def __get_username(cls, tag) -> str:
        player_name_prompt = '{tag} enter your name: '
        keep_trying = True
        while keep_trying:
            try:
                player_name = input(player_name_prompt.format(tag=tag))
                keep_trying = not cls.__validate_username(player_name)
                return player_name
            except Exception as e:
                print(str(e))

    @classmethod
    def __validate_username(cls, username: str) -> bool:
        if username is None:
            raise Exception('Invalid username.')

        username_len = len(username)
        if username_len == 0:
            raise Exception('C\'mon... Please enter someting.')

        if username_len < cls.rules['username']['length']['min']:
            raise Exception('Username too short.')

        if username_len > cls.rules['username']['length']['max']:
            raise Exception('Username too long.')

        return True


if __name__ == '__main__':
    game = ConnectFour2PFactory.build()
    game.run()
