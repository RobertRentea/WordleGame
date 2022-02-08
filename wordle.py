import os
import random

WORDLE_DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'wordle_data'
)

POSSIBLE_WORDS_FILE = os.path.join(WORDLE_DATA_DIR, 'possible_words.txt')
ALLOWED_WORDS_FILE = os.path.join(WORDLE_DATA_DIR, 'allowed_words.txt')

clear = lambda: os.system('clear')

class WordleGame:
    MISS = '⬛'
    MISPLACED = '🟨'
    EXACT = '🟩'

    def __init__(self, word=None) -> None:
        with open(POSSIBLE_WORDS_FILE) as possible_words_file:
            self.possible_words = possible_words_file.read().split('\n')
        with open(ALLOWED_WORDS_FILE) as allowed_words_file:
            self.allowed_words = allowed_words_file.read().split('\n')

        self.word = random.choice(self.possible_words) if word is None else word
        print(self.word)
        self.guesses = []
        self.won = False
        self.show_error_message = False
        self.draw()

    def guess(self, word):
        if word not in self.allowed_words:
            self.show_error_message = True
            self.draw()
            self.show_error_message = False
            return
        if word == self.word:
            self.won = True
        self.guesses.append(word)
        self.draw()

    def finished(self):
        return len(self.guesses) == 6 or self.won

    def draw(self):
        clear()
        print(f'Word: {self.word}')
        print(f'Guesses: {self.guesses}')

        word_rows = []
        for word in self.guesses:
            line = []
            for i, letter in enumerate(word):
                if letter in self.word:
                    if letter == self.word[i]:
                        line.append(self.EXACT)
                    else:
                        line.append(self.MISPLACED)
                else:
                    line.append(self.MISS)
            line = [str(square) for square in line]
            word_rows.append(''.join(line))
        word_rows.extend([''] * (6 - len(self.guesses)))
        for row in word_rows:
            print(row)

        if self.show_error_message:
            print('Not a valid word!')
        else:
            print()

    def play(self):
        try:
            self.draw()
            while not self.finished():
                word = input()
                self.guess(word)
                self.draw()
        except KeyboardInterrupt:
            print()
        if self.won:
            print(f'Congratulation! You have guessed the word in {len(self.guesses)} guess{"es" if len(self.guesses) > 1 else ""}.')
        else:
            print(f'Better luck next time.')


if __name__ == "__main__":
    game = WordleGame()
    try:
        while not game.finished():
            word = input('\rEnter your word: ')
            game.guess(word)
    except KeyboardInterrupt:
        print()



