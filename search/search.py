# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    stack = util.Stack()

    #a dictionary for the actual node, to know at every moment his state, his parent and his next action
    actual_node = {'state': problem.getStartState() , 'parent': None , 'action': None} 
    goal_node = {} #we will save the goal state node on this node

    visited = set()
    stack.push(actual_node)

    while not stack.isEmpty():
        actual_node = stack.pop()
        if actual_node['state'] in visited:
            continue
        visited.add(actual_node['state'])

        if problem.isGoalState(actual_node['state']): #if its the last one
            goal_node = actual_node # we got the final path! keep the last node to the goal_node dictionary
            break

        for successor in problem.getSuccessors(actual_node['state']):
            if successor[0] not in visited: #if its visited it wont create a new one, so in the next loop we will pop the one before
                child_node = {'state': successor[0], 'parent':actual_node , 'action':successor[1]}
                stack.push(child_node)
    
    #now we have the moves in 'action' of each goal_node, just save it in a list and reverse it.
    path = []
    while goal_node['action'] != None:
        path.append(goal_node['action'])
        goal_node = goal_node['parent']

    path.reverse()
    return path

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #now we use queues (FIFO) Same as dfs but with queue
    queue = util.Queue()

    actual_node = {'state': problem.getStartState() , 'parent': None , 'action': None} 
    goal_node = {}

    visited = []
    queue.push(actual_node)

    while not queue.isEmpty():
        actual_node = queue.pop()
        if actual_node['state'] in visited:
            continue
        visited.append(actual_node['state'])

        if problem.isGoalState(actual_node['state']):
            goal_node = actual_node
            break

        for successor in problem.getSuccessors(actual_node['state']):
            if successor[0] not in visited: 
                child_node = {'state': successor[0], 'parent':actual_node , 'action':successor[1]}
                queue.push(child_node)
    
    path = []
    while goal_node['action'] != None:
        path.append(goal_node['action'])
        goal_node = goal_node['parent']


    path.reverse()
    #print path

    return path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    priqueue = util.PriorityQueue()

    #we add a new attribute in the dictionary 'cost' to know the actual cost of the path in this node
    actual_node = {'state': problem.getStartState() , 'parent': None , 'action': None, 'cost':0} 
    goal_node = {}

    visited = set()
    priqueue.push(actual_node, actual_node['cost'])

    while not priqueue.isEmpty():
        actual_node = priqueue.pop()
        if actual_node['state'] in visited:
            continue
        visited.add(actual_node['state'])
        
        #print actual_node
        if problem.isGoalState(actual_node['state']):
            goal_node = actual_node
            break

        for successor in problem.getSuccessors(actual_node['state']):
            if successor[0] not in visited: #if has not been visited we create a new child and now with the cost attribute + the actual cost of the current path (saved in the cost of the parent node)
                child_node = {'state': successor[0], 'parent':actual_node , 'action':successor[1] , 'cost':successor[2] + actual_node['cost']}
                priqueue.push(child_node, child_node['cost'])
    
    #now we have the moves in 'action' of each , just save it in a list and reverse it.
    path = []
    while goal_node['action'] != None:
        path.append(goal_node['action'])
        goal_node = goal_node['parent']


    path.reverse()
    #print path

    return path

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    priqueue = util.PriorityQueue()

    actual_node = {'state': problem.getStartState() , 'parent': None , 'action': None, 'cost':0, 'value':heuristic(problem.getStartState(),problem)} 
    goal_node = {}
    visited = set()
    priqueue.push(actual_node, actual_node['cost'] + actual_node['value'])


    while not priqueue.isEmpty():
        actual_node = priqueue.pop()
        if actual_node['state'] in visited:
            continue
        visited.add(actual_node['state'])
        
        if problem.isGoalState(actual_node['state']):
            goal_node = actual_node
            break

        for successor in problem.getSuccessors(actual_node['state']):
            if successor[0] not in visited: #if has not been visited we create a new child and now with the cost attribute + the actual cost of the current path (saved in the cost of the parent node)
                child_node = {'state': successor[0], 'parent':actual_node , 'action':successor[1] , 'cost':successor[2] + actual_node['cost'] , 'value':heuristic(successor[0],problem)}
                priqueue.push(child_node, child_node['cost'] + child_node['value'])
    
    
    path = []
    while goal_node['action'] != None:
        path.append(goal_node['action'])
        goal_node = goal_node['parent']


    path.reverse()
    #print path

    return path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
