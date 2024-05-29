from graphics import * 
import numpy as np
# The 'chess' refers to the 'stone' that players use, (either black or white)
# I will change the text at the end


SIZE = 15                   # size of the board (square by default)
CONNECT_N = 5               # number of chess in a row to win the game, you can change this to test
BOX_WIDTH = 50              # width of an individual box
NUM_COLUMN = SIZE
NUM_ROW = SIZE
CHESS_RADIUS = 20           # radius of chess


player1_list = []  
player2_list = []  
all_list = []  




def create_window():
    # Create the game board 
    window = GraphWin("Gomoku", BOX_WIDTH * NUM_COLUMN, BOX_WIDTH * NUM_ROW)
    window.setBackground("light blue")

    for vertical_iterator in range(0, BOX_WIDTH * NUM_COLUMN + 1, BOX_WIDTH):
        line = Line(Point(vertical_iterator, 0), Point(vertical_iterator, BOX_WIDTH * NUM_COLUMN))
        line.draw(window)

    for horizontal_iterator in range(0, BOX_WIDTH * NUM_ROW + 1, BOX_WIDTH):
        line = Line(Point(0, horizontal_iterator), Point(BOX_WIDTH * NUM_ROW, horizontal_iterator))
        line.draw(window)

    return window






def rotateMatrix(matrix):
    ## helper function that rotates the matrix so the diagonals are converted to rows
    ## helper function for 'game_over()'
    ## this function is generated by ChatGPT
    n = matrix.shape[0]  
    max_length = 2 * n - 1 
    diagonal_matrix = []

    for offset in range(-n + 1, n):
        diag = matrix.diagonal(offset=offset)
        padding = [0] * (max_length - len(diag))
        padded_diag = padding[:len(padding)//2] + list(diag) + padding[len(padding)//2:]
        diagonal_matrix.append(padded_diag)

    for offset in range(-n + 1, n):
        diag = np.fliplr(matrix).diagonal(offset=offset)
        padding = [0] * (max_length - len(diag))
        padded_diag = padding[:len(padding)//2] + list(diag) + padding[len(padding)//2:]
        diagonal_matrix.append(padded_diag)

    weights = np.array([2**i for i in range(max_length)])
    win_values = [sum(weights[i:i+CONNECT_N]) for i in range(len(weights) - CONNECT_N + 1)]

    return (np.array(diagonal_matrix), weights, win_values)



def game_over(player_list):
    '''
    Parameter:
    @player_list: the list that stores the corrdinates of the chess that current player placed

    Algorithm from
    https://cs.stackexchange.com/questions/86999/how-to-validate-a-connect-x-game-tick-tak-toe-gomoku
    I think it's really cool as it can check any number of chess in row for win condition
    '''
    matrix = np.zeros((NUM_ROW, NUM_COLUMN))
    for row, col in player_list:
        matrix[row, col] = 1

    weights = np.array([2**i for i in range(NUM_ROW)])
    win_values = [sum(weights[i:i+CONNECT_N]) for i in range(len(weights) - CONNECT_N + 1)]

    ### Horiziontal
    if any(value in win_values for value in np.dot(matrix, weights)):
        return True
    
    ### Vertical
    if any(value in win_values for value in np.dot(matrix.T, weights)):
        return True

    ### Diagonally
    result = rotateMatrix(matrix)
    if any(value in result[2] for value in np.dot(result[0], result[1])):
        return True

    return False


# -----------------------------------------------------------------------------------------------------
### May 19th

def ai_pos():
    next_pos = []
    alpha = -float('inf')
    beta = float('inf')
    _, next_pos = Max(next_pos, alpha, beta, depth=0)
    return next_pos[0], next_pos[1]



def Max(state, alpha, beta, depth=0):
    if game_over(player1_list) or game_over(player2_list) or depth == 4:
        return eval(all_list), None

    value = -float('inf')
    best_move = None

    for child in get_children(state):  # child is the state of playboard, list of lists
        eval_child, _ = Min(child, alpha, beta, depth + 1)
        if eval_child > value:
            value = eval_child
            best_move = child[-1]
        alpha = max(alpha, value)
        if value >= beta:
            break

    return value, best_move


def Min(state, alpha, beta, depth=0):
    if game_over(player1_list) or game_over(player2_list) or depth == 4:
        return eval(all_list), None

    value = float('inf')
    best_move = None

    for child in get_children(state):  # child is the state of playboard, list of lists
        eval_child, _ = Max(child, alpha, beta, depth + 1)
        if eval_child < value:
            value = eval_child
            best_move = child
        beta = min(beta, value)
        if value <= alpha:
            break

    return value, best_move


def get_children(state):
    children = []
    for row in range(NUM_ROW):
        for col in range(NUM_COLUMN):
            if (row, col) not in state:
                new_state = state.copy()  
                new_state.append((row, col))
                children.append(new_state)  
    return children
# -----------------------------------------------------------------------------------------------------

def play_the_chess():
    '''
    main function that starts the game
    '''
    
    window = create_window()

    turn = 0
    is_gameOver = False

    while not is_gameOver:
        
        if turn % 2 == 0:
            pos1 = window.getMouse()                    # replace human's choice with AI's choice after implementing the algo
            pos1_X = round((pos1.getX()) / BOX_WIDTH)
            pos1_Y = round((pos1.getY()) / BOX_WIDTH)

            if not ((pos1_X, pos1_Y) in all_list):
                player1_list.append((pos1_X, pos1_Y))
                all_list.append((pos1_X, pos1_Y))

                piece = Circle(Point(BOX_WIDTH * pos1_X, BOX_WIDTH * pos1_Y), CHESS_RADIUS)
                piece.setFill('black')
                piece.draw(window)

                if game_over(player1_list):
                    message = Text(Point(600, 40), "black win.")
                    message.setSize(20)
                    message.draw(window)
                    message.setStyle('bold italic')
                    is_gameOver = True

                turn += 1

        else:
            pos2 = window.getMouse()
            pos2_X = round((pos2.getX()) / BOX_WIDTH)
            pos2_Y = round((pos2.getY()) / BOX_WIDTH)

            if not ((pos2_X, pos2_Y) in all_list):
                player2_list.append((pos2_X, pos2_Y))
                all_list.append((pos2_X, pos2_Y))

                piece = Circle(Point(BOX_WIDTH * pos2_X, BOX_WIDTH * pos2_Y), CHESS_RADIUS)
                piece.setFill('white')
                piece.draw(window)

                if game_over(player2_list):
                    message = Text(Point(600, 40), "white win.")
                    message.setSize(20)
                    message.setStyle('bold italic')
                    message.draw(window)
                    is_gameOver = True

                turn += 1

    window.getMouse()
    window.close()

# ----------------------------------------------------------------------------
### IGNORE IT: There are still error with background music
# from playsound import playsound
# import threading

# def play_music():
#     while True:
#         playsound('music.mp3')

# thread = threading.Thread(target=play_music)
# thread.start()
# ----------------------------------------------------------------------------

play_the_chess()

