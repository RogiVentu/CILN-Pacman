# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        #print newPos, ", " ,  newFood,", ", newGhostStates,", " ,newScaredTimes, "./"
        score = successorGameState.getScore()
        x,y = newPos[0], newPos[1]
        all_h = [] #for heuristics
        min_h = 0 #for smallest heuristic

        #here we check the actual distance between food and current position and then subtrack the minimum to the score
        for food in newFood.asList():
            all_h.append(manhattanDistance(food,newPos))
        if len(all_h) != 0:
            min_h = min(all_h) #we want the less expensive heuristic
        score = score - min_h

        all_gh = []
        min_gh = 0
        ghost_pos = successorGameState.getGhostPositions()

        for gp in ghost_pos:
            all_gh.append(manhattanDistance(gp,newPos))
        min_gh = min(all_gh)
        score = score + min_gh

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #there we define 2 methods that represent min_value:ghosts players and max_value: pacman player. 
        def min_value(gameState, depth, ghostIndex): #min player method, the ghosts.
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState);

            min_aux = float('Inf')
            numGhosts = gameState.getNumAgents()-1 #because we just want the ghosts
            #as the labs says: the minimax tree will have multiple min layers (one for each ghost) for every max layer.
            #so we need to recursively all the ghosts and the last one just call max_value method.
            for action in gameState.getLegalActions(ghostIndex):
                if ghostIndex is not numGhosts:
                    min_aux = min(min_aux , min_value(gameState.generateSuccessor(ghostIndex, action), depth, ghostIndex+1))
                else:
                    min_aux = min(min_aux , max_value(gameState.generateSuccessor(ghostIndex, action), depth+1))
            return min_aux

        def max_value(gameState, depth): #max player method, pacman.
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            max_aux = float('-Inf')
            for action in gameState.getLegalActions(0): #0 because its Pacman
                #compare actual max with the min value of the successors from each action, and then this will be recursivea and will get the minimun value
                max_aux = max(max_aux , min_value(gameState.generateSuccessor(0, action), depth, 1)) # 1 because ghostIndex its >=1
            return max_aux

        #here we get the action with max value using the 2 methods before
        min_value_action = [] #we store here a touples of (value,action)
        for action in gameState.getLegalActions(0):
            min_value_action.append((min_value(gameState.generateSuccessor(0, action), 0, 1), action)) #with depth = 0
        return max(min_value_action,key=lambda item:item[0])[1] #return the action with max value

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def min_value(gameState, depth, ghostIndex, alpha, beta): #min player method, the ghosts.
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState);

            min_aux = float('Inf')
            numGhosts = gameState.getNumAgents()-1 
            for action in gameState.getLegalActions(ghostIndex):
                if ghostIndex is not numGhosts:
                    min_aux = min(min_aux , min_value(gameState.generateSuccessor(ghostIndex, action), depth, ghostIndex+1, alpha, beta))
                else:
                    min_aux = min(min_aux , max_value(gameState.generateSuccessor(ghostIndex, action), depth+1, alpha, beta))
                if min_aux < alpha:
                    return min_aux
                beta = min(beta, min_aux)
            return min_aux

        def max_value(gameState, depth, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            max_aux = float('-Inf')
            for action in gameState.getLegalActions(0):
                max_aux = max(max_aux , min_value(gameState.generateSuccessor(0, action), depth, 1,alpha,beta))
                if max_aux > beta:
                    return max_aux
                alpha = max(alpha, max_aux)
            return max_aux

        min_value_action = [] 
        alpha =float('-Inf')
        beta = float('Inf')
        for action in gameState.getLegalActions(0):
            min_value_action.append((min_value(gameState.generateSuccessor(0, action), 0, 1, alpha, beta), action))

            #we chech here the maximum value of the actions done for now, and if there are a value higher than beta
            #we return the action
            max_val = max(min_value_action,key=lambda item:item[0])[0]
            max_action = max(min_value_action,key=lambda item:item[0])[1]
            if max_val > beta:
                return max_action
            #then we change the alpha if its bigger than the actual alpha
            alpha = max(alpha, max_val)

        return max(min_value_action,key=lambda item:item[0])[1]

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

