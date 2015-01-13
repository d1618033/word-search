import random
import string


DIRECTIONS = ['up', 'down', 'left', 'right',
              'right_up_diag', 'right_down_diag',
              'left_up_diag', 'left_down_diag']
DIRECTION_TO_FUNC = {"up": lambda board, i, j, n: None if i - n + 1 < 0 else [(k, j) for k in range(i, i - n, -1)],
                     "down": lambda board, i, j, n: None if i + n - 1 >= len(board) else [(k, j) for k in range(i, i + n)],
                     "left": lambda board, i, j, n: None if j - n + 1 < 0 else [(i, k) for k in range(j, j - n, -1)],
                     "right": lambda board, i, j, n: None if j + n - 1 >= len(board[0]) else [(i, k) for k in range(j, j + n)],
                     "right_up_diag": lambda board, i, j, n: None if j + n - 1 >= len(board[0]) or i - n + 1 < 0 else [(L, k) for L, k in zip(range(i, i - n, -1), range(j, j + n))],
                     "right_down_diag": lambda board, i, j, n: None if j + n - 1 >= len(board[0]) or i + n - 1 >= len(board) else [(L, k) for L, k in zip(range(i, i + n), range(j, j + n))],
                     "left_up_diag": lambda board, i, j, n: None if j - n + 1 < 0 or i - n + 1 < 0 else [(L, k) for L, k in zip(range(i, i - n, -1), range(j, j - n, -1))],
                     "left_down_diag": lambda board, i, j, n: None if j - n + 1 < 0 or i + n - 1 >= len(board) else [(L, k) for L, k in zip(range(i, i + n), range(j, j - n, -1))]}


def letters_in_dir(board, i, j, n, direction):
    """(list, int, int, int, string) -> list
    returns a list of  the letters in the board
    starting from i and j and going n steps in direction
    returns None if goes out of bounds
    """
    indices = DIRECTION_TO_FUNC[direction](board, i, j, n)
    return None if indices is None else [board[K][L] for K, L in indices]


def can_fit_in_dir(word, board, i, j, direction):
    """(string, list, int, int, string) -> bool
    returns True iff word can be put in board
    at row i, column j in direction"""
    letters = letters_in_dir(board, i, j, len(word), direction)
    return not letters is None and all([lb == '' or lb == lw for lb, lw in zip(letters, word)])


def dirs_to_fit(word, board, i, j):
    """(string, list, int, int) -> list of string
    returns the direction that the word can fit in board
    at row i, column j, (if there isn't - returns empty list)
    """
    return [d for d in DIRECTIONS if can_fit_in_dir(word, board, i, j, d)]


def fit_word_in_dir(word, board, i, j, direction):
    """(string, list, int, int, string) -> boolean
    fits a word in the board starting from row i, column j in direction
    returns True iff can fit
    """
    indices = DIRECTION_TO_FUNC[direction](board, i, j, len(word))
    if indices is None:
        return False
    for index, (K, L) in enumerate(indices):
        board[K][L] = word[index]
    return True


def fit_word_in_random_dir(word, board, i, j):
    """(list, int, int, int) -> boolean
    fits a word in the board starting from row i, column j
    returns True iff can fit, else returns direction
    """
    random.shuffle(DIRECTIONS)
    for d in dirs_to_fit(word, board, i, j):
        if fit_word_in_dir(word, board, i, j, d):
            return d
    return False


def fit_word_in_random_loc(word, board):
    """(list, int) -> boolean
    fits a word in the board
    returns i, j, direction iff can fit else False
    """
    indices = [(i, j) for i in range(len(board)) for j in range(len(board[0]))]
    random.shuffle(indices)
    for i, j in indices:
        d = fit_word_in_random_dir(word, board, i, j)
        if d:
            return i, j, d
    return False


def clear_word(word, board, i, j, direction):
    indices = DIRECTION_TO_FUNC[direction](board, i, j, len(word))
    for K, L in indices:
        board[K][L] = ''


def fit_words(board, words, i=0):
    if i == len(words):
        return True
    word = words[i]
    place = fit_word_in_random_loc(word, board)
    if not place:
        return False
    if not fit_words(board, words, i + 1):
        clear_word(word, board, *place)
        return False
    return True


def main(words, board_size=None):
    if board_size is None:
        board_size = max([len(word) for word in words])
    while True:
        board = [['' for j in range(board_size)] for i in range(board_size)]
        if fit_words(board, words):
            break
        board_size += 1
    board = [[letter if letter != '' else random.choice(string.ascii_uppercase) for letter in row] for row in board]
    return board


def html_table(boards):
    html = []
    html.append(' <head> <style> table,th,td { border:1px solid black; border-collapse:collapse; text-align:center;} th,td{ padding:15px;}</style> </head>')
    for board in boards:
        html.append('<table style="width:100px"><tbody>')
        for row in board:
            html.append('<tr>')
            for col in row:
                html.append('<td>')
                html.append(str(col))
                html.append('</td>')
            html.append('</tr>')
        html.append('</tbody></table>')
        for i in range(3):
            html.append('<br/>')
    return '\n'.join(html)


if __name__ == "__main__":
    from sys import stdin, argv
    if len(argv) >= 2:
        board_size = int(argv[1])
    else:
        board_size = None
    words = []
    boards = []
    for word in stdin:
        word = word.strip().upper()
        if word == '':
            boards.append(main(words, board_size))
            words = []
        else:
            words.append(word)
    boards.append(main(words, board_size))
    print(html_table(boards))
