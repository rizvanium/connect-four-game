from domain.colors import Bcolors
from enum import Enum


class Token:
    def __init__(self, token_name: str, color_val: str) -> None:
        self.name = token_name
        self.color = color_val

    def get_name(self) -> str:
        return self.name

    def get_color(self) -> str:
        return self.color


class Tokens(Enum):
    P1 = Token('P1', Bcolors.RED)
    P2 = Token('P2', Bcolors.YELLOW)
