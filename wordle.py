import os
import random

WORDLE_DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data'
)

POSSIBLE_WORDS_FILE = os.path.join(WORDLE_DATA_DIR, 'possible_words.txt')
ALLOWED_WORDS_FILE = os.path.join(WORDLE_DATA_DIR, 'allowed_words.txt')

clear = lambda: os.system('clear')

class Pattern:
    '''A pattern is encoded using the following convention:
        0 - the letter is not in the word (dark grey)
        1 - the letter is in the word, but on a different location (yellow)
        2 - the letter is in the correct location (green)
    '''
    MISS = '⬛'
    MISPLACED = '🟨'
    EXACT = '🟩'

    def __init__(self, word: str, guessed_word: str) -> None:
        guessed_word = list(guessed_word)
        word = list(word)
        self._pattern = [-1] * 5
        for i, letter in enumerate(guessed_word):
            if letter == word[i]:
                self._pattern[i] = 2
                word[i] = '_'
            elif letter not in word:
                self._pattern[i] = 0

        for i, letter in enumerate(guessed_word):
            if self._pattern[i] != -1:
                continue
            if letter not in word:
                self._pattern[i] = 0
            else:
                self._pattern[i] = 1
                word[word.index(letter)] = '_'

    @property    
    def pattern(self):
        return self._pattern
    
    def __str__(self) -> str:
        pattern = ''
        for type in self._pattern:
            if type == 0:
                pattern += self.MISS
            elif type == 1:
                pattern += self.MISPLACED
            elif type == 2:
                pattern += self.EXACT
        return pattern
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Pattern):
            return False
        return __o.pattern == self.pattern

    def __hash__(self) -> int:
        return hash(''.join([str(type) for type in self._pattern]))

class WordleGame:

    def __init__(self, word=None) -> None:
        with open(POSSIBLE_WORDS_FILE) as possible_words_file:
            self.possible_words = possible_words_file.read().split('\n')
        with open(ALLOWED_WORDS_FILE) as allowed_words_file:
            self.allowed_words = allowed_words_file.read().split('\n')

        self.word = random.choice(self.possible_words) if word is None else word
        self.guesses = []
        self.won = False
        self.show_error_message = False
        self.draw()

    def guess(self, word):
        if word not in self.allowed_words:
            self.show_error_message = True
            self.draw()
            self.show_error_message = False
            return None
        if word == self.word:
            self.won = True
        self.guesses.append(word)
        self.draw()

        return Pattern(self.word, word)

    def finished(self):
        return len(self.guesses) == 6 or self.won

    def draw(self):
        clear()
        print(f'Word: {self.word}')
        print(f'Guesses: {self.guesses}')

        word_rows = []
        for guessed_word in self.guesses:
            pattern = Pattern(self.word, guessed_word)
            word_rows.append(str(pattern))
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




