from graphics import *
import numpy as np
import time

# The 'chess' refers to the 'stone' that players use, (either black or white)
# I will change the text at the end


SIZE = 15  # size of the board (square by default)
CONNECT_N = 5  # number of chess in a row to win the game, you can change this to test
BOX_WIDTH = 50  # width of an individual box
NUM_COLUMN = SIZE
NUM_ROW = SIZE
CHESS_RADIUS = 20  # radius of chess
MAX_DEPTH = 2  # can be only either 1 or 2 for now

player1_list = []
player2_list = []
all_list = []

cut_count = 0
total_time = 0
step_times = []

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
    n, m = matrix.shape
    diagonal_matrix = []

    # Top-left to bottom-right diagonals
    for offset in range(-n + 1, m):
        diag = np.diagonal(matrix, offset=offset)
        padded_diag = np.pad(diag, (max(0, -offset), max(0, offset)), 'constant', constant_values=(0, 0))
        diagonal_matrix.append(padded_diag)

    # Top-right to bottom-left diagonals
    flipped_matrix = np.fliplr(matrix)
    for offset in range(-n + 1, m):
        diag = np.diagonal(flipped_matrix, offset=offset)
        padded_diag = np.pad(diag, (max(0, -offset), max(0, offset)), 'constant', constant_values=(0, 0))
        diagonal_matrix.append(padded_diag)

    max_length = max(len(row) for row in diagonal_matrix)
    diagonal_matrix = [np.pad(row, (0, max_length - len(row)), 'constant', constant_values=(0, 0)) for row in
                       diagonal_matrix]

    weights = np.array([2 ** i for i in range(max_length)])
    win_values = [sum(weights[i:i + CONNECT_N + offset]) for offset in range(5) for i in
                  range(len(weights) - CONNECT_N - offset + 1)]

    return (np.array(diagonal_matrix), weights, win_values)


def game_over(player_list):
    '''
    Parameter:
    @player_list: the list that stores the coordinates of the chess that current player placed

    Algorithm from
    https://cs.stackexchange.com/questions/86999/how-to-validate-a-connect-x-game-tick-tak-toe-gomoku
    I think it's really cool as it can check any number of chess in row for win condition
    '''
    matrix = np.zeros((NUM_ROW, NUM_COLUMN))
    for row, col in player_list:
        matrix[row, col] = 1

    weights = np.array([2 ** i for i in range(NUM_COLUMN)])
    win_values = [sum(weights[i:i + CONNECT_N + offset]) for offset in range(5) for i in
                  range(len(weights) - CONNECT_N - offset + 1)]

    ### Horizontal
    if any(value in np.dot(matrix, weights) for value in win_values):
        return True

    ### Vertical
    if any(value in np.dot(matrix.T, weights) for value in win_values):
        return True

    ### Diagonally
    result = rotateMatrix(matrix)
    if any(value in np.dot(result[0], result[1]) for value in result[2]):
        return True

    return False


## check if each point has neighbor
def has_neighbor(pt, board, radius=1):
    for i in range(-radius, radius + 2):
        for j in range(-radius, radius + 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1] + j) in board:
                return True
    return False

def order(empty_positions):
    last_pt = all_list[-1]
    prioritized_list = []
    for point in empty_positions:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor = (last_pt[0] + i, last_pt[1] + j)
                if neighbor in empty_positions:
                    if neighbor not in prioritized_list:
                        prioritized_list.insert(0, neighbor)
    for point in empty_positions:
        if point not in prioritized_list:
            prioritized_list.append(point)
    return prioritized_list

def AI_algo():
    global total_time, step_times
    ## calculate running time
    start_time = time.time()
    next_pos = []
    alpha = -float('inf')
    beta = float('inf')
    _, next_pos = Max(all_list, alpha, beta, depth=0)
    end_time = time.time()

    time_taken = end_time - start_time
    total_time += time_taken
    step_times.append(time_taken)
    ## print(f"AI chose position: {next_pos}")
    print(f"AI chose position: {next_pos} in {time_taken:.4f} seconds")
    return next_pos[0], next_pos[1]

transition_table = {}
def Max(state, alpha, beta, depth=0):
    global cut_count
    board_tuple = tuple(map(tuple, state))

    if board_tuple in transition_table:
        return transition_table[board_tuple], None

    print(f"Max called with depth={depth}, state={state}, alpha={alpha}, beta={beta}")
    if game_over(player1_list) or game_over(player2_list) or depth == MAX_DEPTH:
        player1_list_copy = player1_list.copy()
        player2_list_copy = player2_list.copy()

        evaluation = eval(state, player1_list_copy, player2_list_copy, isAI=False)
        # print(f"Game over or max depth reached, evaluation={evaluation}")
        return evaluation, None

    value = -float('inf')
    best_move = None

    for child in get_children(state):  # child is the state of playboard, list of lists
        if MAX_DEPTH == 1:
            eval_child, _ = Min(child, alpha, beta, depth + 1)
        if MAX_DEPTH == 2:
            eval_child, best_move = Min(child, alpha, beta, depth + 1)
        else:
            eval_child, _ = Min(child, alpha, beta, depth + 1)
        # print(f"Evaluating child in Max: {child}, eval_child={eval_child}")
        if eval_child > value:
            value = eval_child
            best_move = child[-1]
        alpha = max(alpha, value)
        if value >= beta:
            cut_count += 1
            print(f'MAX cut counts: {cut_count}')
            break
    transition_table[board_tuple] = value
    print(f"Max returning value={value}, best_move={best_move}")
    return value, best_move


def Min(state, alpha, beta, depth=0):
    global cut_count
    board_tuple = tuple(map(tuple, state))

    if board_tuple in transition_table:
        return transition_table[board_tuple], None

    # print(f"Min called with depth={depth}, state={state}, alpha={alpha}, beta={beta}")
    if game_over(player1_list) or game_over(player2_list) or depth == MAX_DEPTH:
        player1_list_copy = player1_list.copy()
        player2_list_copy = player2_list.copy()

        evaluation = eval(state, player1_list_copy, player2_list_copy, isAI=True)
        # print(f"Game over or max depth reached, evaluation={evaluation}")
        return evaluation, None

    value = float('inf')
    best_move = None

    for child in get_children(state):  # child is the state of playboard, list of lists
        if MAX_DEPTH == 1:
            eval_child, _ = Max(child, alpha, beta, depth + 1)
        elif MAX_DEPTH == 2:
            eval_child, best_move = Max(child, alpha, beta, depth + 1)
        else:
            eval_child, _ = Max(child, alpha, beta, depth + 1)
        print(f"Evaluating child in Min: {child}, eval_child={eval_child}")
        if eval_child < value:
            value = eval_child
            best_move = child[-1]
        beta = min(beta, value)
        if value <= alpha:
            cut_count += 1
            print(f'MIN cut counts: {cut_count}')
            break
    transition_table[board_tuple] = value
    print(f"Min returning value={value}, best_move={best_move}")
    return value, best_move

def get_children(state):
    empty_positions = [(row, col) for row in range(NUM_ROW) for col in range(NUM_COLUMN) if (row, col) not in state]
    ordered_blanks = order(empty_positions)
    children = []
    for pos in ordered_blanks:
        new_state = state.copy()
        new_state.append(pos)
        if has_neighbor(pos, state):
            children.append(new_state)
    # print(f"Generated children: {children}")
    return children

eval_score = {
    (0, 0, 0, 1, 0, 0): 20,
    (0, 0, 1, 0, 0, 0): 20,
    (0, 0, 1, 0, 1, 0): 120,
    (0, 1, 0, 1, 0, 0): 120,
    (0, 0, 1, 1, 0, 0): 120,
    (1, 1, 1, 0, 1): 720,
    (1, 0, 1, 1, 1): 720,
    (1, 1, 0, 1, 1): 720,
    (0, 1, 1, 1, 1): 720,
    (1, 1, 1, 1, 0): 720,
    (0, 1, 0, 1, 1, 0): 720,
    (0, 1, 1, 0, 1, 0): 720,
    (0, 0, 1, 1, 1, 0): 720,
    (0, 1, 1, 1, 0, 0): 720,
    (0, 1, 1, 1, 1, 0): 4320,
    (1, 1, 1, 1, 1): 99999999
}

def find_score(list1, list2):
    directions = [
        (1, 0),  ## check from (0,3) to (0,4), (3,5)
        (0, 1),  ## check from
        (1, 1),  ## check from (3,3) to (4,4), (5,5)
        (1, -1)  ## check from (3,3) to (2,4), (3,5)
    ]

    total_score = 0  ## total score in the whole list

    out_of_board_positions = ([(i, -1) for i in range(-1, 16)] +
                              [(-1, i) for i in range(-1, 16)] +
                              [(i, 16) for i in range(-1, 16)] +
                              [(16, i) for i in range(-1, 16)])
    check_exist = []
    for point in list1:
        m = point[0]
        n = point[1]
        cur_score = 0  ## score at one point in 4 directions
        already_scored = []
        score_shape = (0, None)
        for x_directions, y_directions in directions:
            ## check if this shape is duplicate
            ## eg. [(2,3), (2,4)]
            ## (2,3) will have [(2,1), (2,2), (2,3), (2,4), (2,5), (2,6)], which is (0,0,1,1,0,0)
            ## (2,4) will also iterate the above
            ## so there is a duplicate
            is_duplicate = False
            for item in check_exist:
                for pt in item[2]:
                    if m == pt[0] and n == pt[1] and x_directions == item[0][0] and y_directions == item[0][1]:
                        is_duplicate = True
                        break
                if is_duplicate:
                    break
            if is_duplicate:
                continue

            matrix_fiv = []
            matrix_six = []

            max_score = 0  ## score at one point in one direction
            new_shape = []  ## new shape for max score

            ## consider point = (2,3) in direction (1,0)
            ## ① [(2,-2), (2,-1), (2,0), (2,1), (2,2), (2,3)] => (-1,-1,0,0,0,1)
            ## ② [(2,-1), (2,0), (2,1), (2,2), (2,3), (2,4)]  => (-1,0,0,0,1,0)
            ## ③ [(2,0), (2,1), (2,2), (2,3), (2,4), (2,5)]   => (0,0,0,1,0,0)
            ## ④ [(2,1), (2,2), (2,3), (2,4), (2,5), (2,6)]   => (0,0,1,0,0,0)
            ## ⑤ [(2,2), (2,3), (2,4), (2,5), (2,6), (2,7)]   => (0,1,0,0,0,0)
            ## ⑥ [(2,3), (2,4), (2,5), (2,6), (2,8), (2,9)]   => (1,0,0,0,0,0)
            ## in this case, ③ and ④ score 20 each
            ## but we only take the max at one direction which is 20
            for offset in range(-5, 1):
                check = []
                matrix_pos = []
                for i in range(0, 6):
                    row = m + (i + offset) * x_directions
                    col = n + (i + offset) * y_directions
                    current_position = (row, col)

                    ## if out of board, append -1
                    if current_position in out_of_board_positions:
                        check.append(-1)
                    else:
                        if current_position in list2:
                            check.append(2)
                        elif current_position in list1:
                            check.append(1)
                        else:
                            check.append(0)
                    matrix_pos.append(current_position)
                iteration = (matrix_pos[0], matrix_pos[1], matrix_pos[2], matrix_pos[3], matrix_pos[4], matrix_pos[5])

                ## put them in a tuple
                check_fiv = (check[0], check[1], check[2], check[3], check[4])
                check_six = (check[0], check[1], check[2], check[3], check[4], check[5])

                ## put them into a matrix
                matrix_fiv.append(check_fiv)
                matrix_six.append(check_six)
                for shape in eval_score:

                    score = eval_score[shape]
                    for i in range(len(matrix_fiv)):
                        if i < len(matrix_six):
                            if matrix_fiv[i] == shape or matrix_six[i] == shape:
                                if score > max_score:
                                    max_score = score
                                    new_shape.append(shape)

                                    score_shape = ((x_directions, y_directions), score, iteration)
                        else:
                            if matrix_fiv[i] == shape:
                                if score > max_score:
                                    max_score = score
                                    new_shape.append(shape)
                                    score_shape = ((x_directions, y_directions), score, iteration)
            ## calculate if two shape intersect at one point
            ## than add the score together
            # print(f"Max score in direction {x_directions, y_directions}: {max_score}")
            ## print(f"Max shape in direction {x_directions, y_directions}: {new_shape}")
            if max_score != 0:
                cur_score = max_score + cur_score
                ## print(score_shape)
                check_exist.append(score_shape)
            ## print(matrix_six)
        # print(check_exist)
        # print(f"current score at this point {point}: {cur_score}")

        total_score = total_score + cur_score
    # print(total_score)
    return total_score


def eval(state, player1_list_copy, player2_list_copy, isAI=None):
    human_list = player1_list_copy.copy()
    ai_list = player2_list_copy.copy()
    if isAI:
        ai_list.append(state[-1])
    else:
        human_list.append(state[-1])

    print(f'ai list{ai_list}')
    print(f'human list {human_list}')

    ai_score = find_score(ai_list, human_list)
    human_score = find_score(human_list, ai_list)
    return ai_score - human_score * 0.1


def play_the_chess():
    '''
    main function that starts the game
    '''
    global total_time, step_times
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
                    message.setSize(20)
                    message.draw(window)
                    message.setStyle('bold italic')
                    is_gameOver = True

                turn += 1

        else:
            pos2 = AI_algo()
            pos2_X = pos2[0]
            pos2_Y = pos2[1]

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
    print(f"Total time taken by AI: {total_time:.4f} seconds")
    for i, t in enumerate(step_times):
        print(f"Step {i + 1}: {t:.4f} seconds")
    average_time = total_time / len(step_times)
    print(f"Average time per step: {average_time:.4f} seconds")

play_the_chess()