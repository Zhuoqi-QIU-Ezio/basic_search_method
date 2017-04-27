# heuristics.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

#Zhuoqi QIU u5542244


""" This class contains heuristics which are used for the search procedures that
    you write in search_strategies.py.

    The first part of the file contains heuristics to be used with the algorithms
    that you will write in search_strategies.py.

    In the second part you will write a heuristic for Q4 to be used with a
    MultiplePositionSearchProblem.
"""

#-------------------------------------------------------------------------------
# A set of heuristics which are used with a PositionSearchProblem 
# You do not need to modify any of these.
#-------------------------------------------------------------------------------

def null_heuristic(pos, problem):
    """ The null heuristic. It is fast but uninformative. It always returns 0.
        (State, SearchProblem) -> int
    """
    return 0

def manhattan_heuristic(pos, problem):
  """ The Manhattan distance heuristic for a PositionSearchProblem.
      ((int, int), PositionSearchProblem) -> int
  """
  return abs(pos[0] - problem.goal_pos[0]) + abs(pos[1] - problem.goal_pos[1])

def euclidean_heuristic(pos, problem):
    """ The Euclidean distance heuristic for a PositionSearchProblem
        ((int, int), PositionSearchProblem) -> float
    """
    return ((pos[0] - problem.goal_pos[0]) ** 2 + (pos[1] - problem.goal_pos[1]) ** 2) ** 0.5

#Abbreviations
null = null_heuristic
manhattan = manhattan_heuristic
euclidean = euclidean_heuristic
 
#-------------------------------------------------------------------------------
# You have to implement the following heuristic for Q4 of the assignment.
# It is used with a MultiplePositionSearchProblem
#-------------------------------------------------------------------------------

#You can make helper functions here, if you need them

def every_bird_heuristic(state, problem):
    """ Q4: Find Every Yellow Bird (4 marks)
        
        This heuristic is used for solving a MultiplePositionSearchProblem.
        It should return an estimate of the cost of reaching a goal state in
        problem, from the given state.

        To ensure correctness, this heuristic must be admissible. This means that
        it must not overestimate the cost of reaching the goal. Inadmissible
        heuristics may still find optimal solutions, so be careful.

        The state is a tuple (pos, yellow_birds) where:
            - pos is a tuple (int, int) indicating the red bird's current position;
            - yellow_birds is a tuple ((int, int), (int, int), ...) containing
              tuples representing the positions of the remaining yellow birds.
              
        You have access to the following information directly from problem:
            
            - problem.maze_distance(pos1, pos2)
                (MultiplePositionSearchProblem, (int, int), (int, int)) -> int
            
                This will return the shortest distance between the given positions.
                Do not use this information to for earlier parts of the assignment.
                We will actually look at your code!
                
            - problem.get_width() 
                (MultiplePositionSearchProblem) -> int
                
                This will return the width of the board.
            
            - problem.get_height()
                (MultiplePositionSearchProblem) -> int
                
                This will return the height of the board.
            
            - problem.get_walls()
                (MultiplePositionSearchProblem) -> [[bool]]
                
                This will return lists representing a 2D array of the wall positions.

        If you want to *store* information to be reused in other calls to the heuristic,
        there is a dictionary called problem.heuristic_info that you can use.
        
        You need to be able to explain your heuristic to us -- i.e. what's the
        intuition behind it?
        
        You should comment your heuristic.
        
        Feel free to make helper functions above this one.
        
        (((int, int), ((int, int))), MultiplePositionSearchProblem) -> number
    """
    if problem.heuristic_info.get(state):
        return problem.heuristic_info.get(state)
    position, yellow_birds = state
    heuristic_value = 0
    """ *** YOUR CODE HERE *** """
    min_value=999999
    for i in range(len(yellow_birds)):
        value=problem.maze_distance(position, yellow_birds[i])
        if min_value>value:
            min_value=value
            heuristic_value=i
    #print position,yellow_birds
    return heuristic_value


