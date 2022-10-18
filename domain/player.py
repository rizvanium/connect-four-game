from domain.token import Tokens, Token


class Player:
    def __init__(self, player_name: str, tag: str, token=Tokens.P1.value) -> None:
        self.name = player_name
        self.tag = tag
        self.token = token

    def get_token(self) -> Token:
        return self.token

    def get_username(self) -> str:
        return self.name

    def get_tag(self) -> str:
        return self.tag
