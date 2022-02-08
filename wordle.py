import os
import random

GREEN = '#00FF00'
YELLOW = '#FFFF00'
DARK_GRAY = '#404040'

WORDLE_DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'wordle_data'
)

POSSIBLE_WORDS_FILE = os.path.join(WORDLE_DATA_DIR, 'possible_words.txt')
ALLOWED_WORDS_FILE = os.path.join(WORDLE_DATA_DIR, 'allowed_words.txt')

class WordleGame:
    def __init__(self) -> None:
        with open(POSSIBLE_WORDS_FILE) as possible_words_file:
            self.possible_words = possible_words_file.read().split('\n')
        with open(ALLOWED_WORDS_FILE) as allowed_words_file:
            self.allowed_words = allowed_words_file.read().split('\n')

        self.word = random.choice(self.possible_words)
        

def square(hex_code: str) -> None:
    hex_code = hex_code.strip('#')
    red = int(hex_code[:2], 16)
    green = int(hex_code[2:4], 16)
    blue = int(hex_code[4:6], 16)

    return f"\033[48:2::{red}:{green}:{blue}m  \033[49m"

if __name__ == "__main__":
    WordleGame()

