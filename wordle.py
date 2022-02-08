from operator import truediv
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


class Square:
    def __init__(self, color) -> None:
        self.color = color

    def __str__(self) -> str:
        hex_code = self.color.strip('#')
        red = int(hex_code[:2], 16)
        green = int(hex_code[2:4], 16)
        blue = int(hex_code[4:6], 16)

        return f"\033[48:2::{red}:{green}:{blue}m  \033[49m"


class WordleGame:
    def __init__(self) -> None:
        with open(POSSIBLE_WORDS_FILE) as possible_words_file:
            self.possible_words = possible_words_file.read().split('\n')
        with open(ALLOWED_WORDS_FILE) as allowed_words_file:
            self.allowed_words = allowed_words_file.read().split('\n')

        self.word = random.choice(self.possible_words)
        print(self.word)
        self.guesses = []
        self.won = False

    def guess(self, word):
        print(f'Guess {len(self.guesses) + 1}')
        if word == self.word:
            self.won = True
        self.guesses.append(word)
        self.draw()

    def finished(self):
        return len(self.guesses) == 6 or self.won

    def draw(self):
        for word in self.guesses:
            line = []
            for i, letter in enumerate(word):
                if letter in self.word:
                    if letter == self.word[i]:
                        line.append(Square(GREEN))
                    else:
                        line.append(Square(YELLOW))
                else:
                    line.append(Square(DARK_GRAY))
            line = [str(square) for square in line]
            print(' '.join(line))

    def play(self):
        while not self.finished():
            word = input()
            self.guess(word)
        if self.won:
            print(f'Congratulation! You have guessed the word in {len(self.guesses)} guess{"es" if len(self.guesses) > 1 else ""}.')
        else:
            print(f'Better luck next time.')


if __name__ == "__main__":
    game = WordleGame()
    game.play()


