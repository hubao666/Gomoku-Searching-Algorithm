from graphics import * 

BOX_WIDTH = 50
NUM_COLUMN = 15
NUM_ROW = 15
CHESS_RADIUS = 20

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



def play_the_chess():
    window = create_window()

    turn = 0
    is_gameOver = False

    while not is_gameOver:
        if turn % 2 == 1:
            pos1 = window.getMouse()
            pos1_X = round((pos1.getX()) / BOX_WIDTH)
            pos1_Y = round((pos1.getY()) / BOX_WIDTH)

            if not ((pos1_X, pos1_Y) in all_list):
                player1_list.append((pos1_X, pos1_Y))
                all_list.append((pos1_X, pos1_Y))

                piece = Circle(Point(BOX_WIDTH * pos1_X, BOX_WIDTH * pos1_Y), CHESS_RADIUS)
                piece.setFill('black')
                piece.draw(window)

                # check if game is over

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

                # check if game is over

                turn += 1


play_the_chess()