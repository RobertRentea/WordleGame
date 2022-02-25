import os
import random
import numpy as np

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
    MISS = 0
    MISSPLACED = 1
    EXACT = 2

    DEFAULT_LENGTH = 5

    TYPE_TO_CHAR = {MISS: '⬛', MISSPLACED: '🟨', EXACT: '🟩'}

    def __init__(self, answer: str, guess: str, pattern: list = None) -> None:
        if pattern:
            self._pattern = pattern
        else:
            if answer is None or guess is None:
                return
            n_letters = len(answer)
            answer = list(answer)
            self._pattern = [Pattern.MISS] * n_letters

            # Green pass
            for i in range(n_letters):
                if guess[i] == answer[i]:
                    self._pattern[i] = Pattern.EXACT
                    answer[i] = '_'  # Marking the letter from answer as taken care of
            
            # Yellow pass
            for i in range(n_letters):
                if answer[i] != '_' and guess[i] in answer:
                    pos = answer.index(guess[i])
                    self._pattern[i] = Pattern.MISSPLACED
                    answer[pos] = '_'  # Same as above

    @property    
    def pattern(self):
        return self._pattern

    @staticmethod
    def from_int(pattern_hash: int):
        pattern = []
        curr = pattern_hash
        for _ in range(Pattern.DEFAULT_LENGTH):
            pattern.append(curr % 3)
            curr = curr // 3
        return Pattern(None, None, pattern)

    @staticmethod
    def from_str(pattern: str):
        p = Pattern(None, None)
        p._pattern = [int(x) for x in pattern]
        return p
    
    def __str__(self) -> str:
        pattern = ''
        for type in self._pattern:
            pattern += Pattern.TYPE_TO_CHAR[type]
        return pattern
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Pattern):
            return False
        return __o._pattern == self._pattern

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __hash__(self) -> int:
        a = np.array(self._pattern)
        b = (3**np.arange(len(self._pattern))).astype(np.uint8)
        return int(np.dot(a, b))

class WordleGame:

    def __init__(self, word=None) -> None:
        with open(POSSIBLE_WORDS_FILE) as possible_words_file:
            self.possible_words = possible_words_file.read().split('\n')
        with open(ALLOWED_WORDS_FILE) as allowed_words_file:
            self.allowed_words = allowed_words_file.read().split('\n')

        self.answer = random.choice(self.possible_words) if word is None else word
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
        if word == self.answer:
            self.won = True
        self.guesses.append(word)
        self.draw()

        return Pattern(self.answer, word)

    def finished(self):
        return len(self.guesses) == 6 or self.won

    def draw(self):
        clear()
        print(f'Word: {self.answer}')
        print(f'Guesses: {self.guesses}')

        word_rows = []
        for guessed_word in self.guesses:
            pattern = Pattern(self.answer, guessed_word)
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




