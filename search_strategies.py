# search_strategies.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

# Zhuoqi QIU u5542244

""" This class contains search functions which you are required to implement
    for Q1-Q3 in the assignment.

    Your search algorithms needs to return a list of actions [str] that reaches
    the goal from the start state in the given problem.

    Make sure to implement graph search algorithms. We suggest that you look at
    the lecture notes to find out how to do this.

    In this case, your search algorithms will be passed a SearchProblem as
    defined in search_problems.py. You can take a look at this if you like,
    but all of the methods you will need to use are listed later in this comment.

    In practice, the search algorithms will either be run with a
    PositionSearchProblem or a MultiplePositionSearchProblem.

    In the former case, a state is a tuple (int, int) representing the
    postion of the red bird. In the latter, a state is a tuple
    ((int, int), ((int, int), ...)) containing a tuple representing the
    position of the red bird and the positions of the remaining yellow birds.

    What is important is that in either case state is hashable and can be
    put into a set or used as the key in a dictionary if your algorithms
    require it.

    The methods from problem that you will require are as follows:
        
        - problem.get_initial_state()
            (SearchProblem) -> state

        - problem.goal_test(state)
            (SearchProblem, state) -> bool

        - problem.get_successors(state)
            (SearchProblem, state) -> [(state, str, int)]
        
            Here, the successors are a list of triples (successor, action, cost):
                - successor is a successor to the current state,
                - action is the action required to get there,
                - cost is the cost of the action.

    We suggest that you use the SearchNode class defined in this file to implement
    your searches.
"""

import util, heuristics, frontiers

class SearchNode:
    """ The data structure representing a search node. It has
        state:      A state as defined by the appropriate SearchProblem
        action:     The action that led to this state from its parent
        path_cost:  The cost to get to this state from the start state
        parent:     The parent SearchNode

        This is created for you to use when implementing the search problems
        later in this file. You do not need to modify this.
    """
    
    def __init__(self, state, action, path_cost, parent):
        """ Make a new search node with the given parameters.
            (SearchNode, state, str, int, SearchNode) -> None
        """
        self.state = state
        self.action = action
        self.path_cost = path_cost
        self.parent = parent

    def __str__(self):
        """ Return a string representation of the SearchNode
            (SearchNode) -> str
        """
        return "Node(" + str(self.state) + ", " + str(self.action) + ", " +\
            str(self.path_cost) + ", " + str(self.parent) + ")"
  
#-------------------------------------------------------------------------------
# YOUR CODE STARTS HERE
#-------------------------------------------------------------------------------
 
#You could write some helper methods here. Maybe a generic search function
#to be used by the following searches if you so desire.

def make_list(node):
    result=[]
    while node.parent:
        result.append(node.action)
        node=node.parent
    result.reverse()
    return result
 
def depth_first_search(problem):
    """ Q1: Depth-First-Search (2 marks)
        DFS searches the deepest nodes in the search tree first.
        
        DFS is best implemented with a Stack found in frontiers.py. It can
        be accessed as follows:
            
            stack = frontiers.Stack()
            
        We suggest that you use the SearchNode class which is defined earlier
        in this file.
          
        (SearchProblem) -> [str]
    """
  
    """ *** YOUR CODE HERE *** """
    visited=set()
    stack=frontiers.Stack()
    node=SearchNode(problem.get_initial_state(), None, None, None)
    stack.push(node)
    while not stack.is_empty():
        node=stack.pop()
        if node.state not in visited:
            visited.add(node.state)
            if problem.goal_test(node.state):
                return make_list(node)
            for successor,action,cost in problem.get_successors(node.state):
                new_node=SearchNode(successor, action, cost, node)
                stack.push(new_node)
    return []
    #util.raise_not_defined() #Remove this line when your solution is implemented

def breadth_first_search(problem):
    """ Q2: Breadth-First-Search (2 marks)
        
        BFS search the shallowest nodes in the search tree first.
        
        BFS is best implemented with a Queue found in frontiers.py. It can
        be accessed as follows:
            queue = frontiers.Queue()

        We suggest that you use the SearchNode class which is defined earlier
        in this file.
        
        (SearchProblem) -> [str]
    """

    """ *** YOUR CODE HERE *** """
    visited=set()
    queue=frontiers.Queue()
    node=SearchNode(problem.get_initial_state(), None, None, None)
    queue.push(node)
    while not queue.is_empty():
        node=queue.pop()
        if node.state not in visited:
            visited.add(node.state)
            if problem.goal_test(node.state):
                return make_list(node)
            for successor,action,cost in problem.get_successors(node.state):
                new_node=SearchNode(successor, action, cost, node)
                queue.push(new_node)
    return []


def a_star_search(problem, heuristic=heuristics.null_heuristic):
    """ Q3: A* Search (3 marks)
        
        Search the node that has the lowest combined cost and heuristic first.

        Your A* search will use the heuristic contained in the heuristic argument.
        The heuristics take a state and return an estimate of the cost to reach
        the goal from that state. The heuristics are defined in heuristics.py
        and for this problem include a null_heuristic, a Manhattan heuristic,
        and a Euclidean heuristic.
        
        It can be assumed that the supplied heuristic function will work with
        the state representation of whatever SearchProblem you have been given
        here.
        
        A* is best implemented with a priority queue found in frontiers.py.
        You can use it by having:
        
            queue = frontiers.PriorityQueue()   OR
            queue = frontiers.PriorityQueueWithFunction(evaluation_function)
            
        In the latter case, you will need to define and pass an evaluation function
        which takes a search node and returns an appropriate f value for the node
        using the given heuristic.
        
        You might want to do this to aid in making a generic search function to
        be used for Q1-3. Making such a generic function is not required.
    """

    """ *** YOUR CODE HERE *** """
    visited=set()
    queue=frontiers.PriorityQueue()
    node=SearchNode(problem.get_initial_state(), None, None, None)
    queue.push(node,heuristic(node.state,problem))
    while not queue.is_empty():
        node=queue.pop()
        if node.state not in visited:
            visited.add(node.state)
            if problem.goal_test(node.state):
                return make_list(node)
            for successor,action,cost in problem.get_successors(node.state):
                new_node=SearchNode(successor, action, cost, node)
                queue.push(new_node,heuristic(node.state,problem))
    return []


# Abbreviations to be used elsewhere in the program
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search

