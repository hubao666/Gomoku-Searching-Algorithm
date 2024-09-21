# Gomoku (Five in a Row)
This is a Python project for playing Gomoku with a graphical interface and AI opponent.

## Introduction
The game is played on a 15x15 grid board where two players take turns placing black or 
white stones. The objective is to align five stones in a row either vertically, horizontally, or diagonally.
   - ![img.png](img.png)
   - Above is the initial grid board. 
   - On the top right-hand corner, there is an 'undo' button, 
which is used to retract a false move in a game.
     - Attention! Our undo functionality does not allow undoing twice in one turn, 
and it does not accept undoing and then playing the same move again.
   


## Installation
   - Instructions to ensure Python 3.x is installed and dependencies are installed using `pip`.

## File Structure
- AIvsHuman (AI goes first)
- AIvsHuman (AI goes second)

## Algorithm
- Min-Max
  - A recursive method used for decision-making in two-player zero-sum games (such as chess, tic-tac-toe). The algorithm evaluates all possible moves in the game to choose the best possible strategy. Each node in the game tree represents a state of the game, and two players alternate turns: one trying to maximize their score (Max) and the other trying to minimize the opponent's score (Min).
  - Alpha-Beta pruning is an optimization technique for the Min-Max algorithm. It reduces the number of nodes that need to be evaluated in the game tree, making the algorithm more efficient. The key idea is to "prune" branches that will not affect the final decision. 
  - We aim to look ahead enough to make intelligent moves without overwhelming the system with too many calculations.
While deeper searches can yield better evaluation scores, they do not always translate to better moves in practice. 
Therefore, we optimize the depth to maintain a balance between time cost and move quality.


- Optimization 
  - The `has_neighbor` function checks if a given point has neighboring stones within radius of 1 .
This helps to prioritize moves that are more likely to affect the game outcome. 
  - The `order` function prioritizes potential moves based on their proximity to the last move made. 
This reduces the search space and focuses on more critical moves first.
  


## Contribution
- Pengyu Chen 
  - Optimization
  - Evaluation function (including score parts)
  - Undo button and function
  - Min-Max algorithm (including Alpha-Beta pruning)
  - UI design
    
- Bao Hu 
  - UI design and implementation
  - Game logic and configuration
  - Min-Max algorithm (including Alpha-Beta pruning)
  - Optimization
  
