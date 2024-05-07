from graphics import * 
import numpy as np

BOX_WIDTH = 50
NUM_COLUMN = 15
NUM_ROW = 15
CHESS_RADIUS = 20
CONNECT_N = 5

player1_list = []  
player2_list = []  
all_list = []  


def create_window():
    window = GraphWin("Gomoku", BOX_WIDTH * NUM_COLUMN, BOX_WIDTH * NUM_ROW)
    window.setBackground("light blue")

    for vertical_iterator in range(0, BOX_WIDTH * NUM_COLUMN + 1, BOX_WIDTH):
        line = Line(Point(vertical_iterator, 0), Point(vertical_iterator, BOX_WIDTH * NUM_COLUMN))
        line.draw(window)

    for horizontal_iterator in range(0, BOX_WIDTH * NUM_ROW + 1, BOX_WIDTH):
        line = Line(Point(0, horizontal_iterator), Point(BOX_WIDTH * NUM_ROW, horizontal_iterator))
        line.draw(window)

    return window



def game_over(player_list):
    '''
    Algorithm from
    https://cs.stackexchange.com/questions/86999/how-to-validate-a-connect-x-game-tick-tak-toe-gomoku
    I think it's really cool
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

    ### implement diagonal direction

    return False






def play_the_chess():
    window = create_window()

    turn = 0
    is_gameOver = False

    while not is_gameOver:
        if turn % 2 == 0:
            pos1 = window.getMouse()
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
                    message.draw(window)
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
                    message.draw(window)
                    is_gameOver = True

                turn += 1

    window.getMouse()
    window.close()


play_the_chess()

