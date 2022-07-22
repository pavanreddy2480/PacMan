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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        l=[]
        for state in newGhostStates:
            dist=manhattanDistance(newPos,state.getPosition()) 
            l.append(dist)
        min_distance=min(l);
        score_difference = successorGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        l=[]
        for food in currentGameState.getFood().asList():
            dist=manhattanDistance(pos,food)
            l.append(dist)
        nearestFoodDistance=min(l)
        newFoodsDistances=[]
        for food in newFood.asList():
            dist=manhattanDistance(newPos,food)
            newFoodsDistances.append(dist)
        if  len(newFoodsDistances)==0:
            newNearestFoodDistance=0
        else:
            newNearestFoodDistance=min(newFoodsDistances)

        nearfood = nearestFoodDistance - newNearestFoodDistance
        direction = currentGameState.getPacmanState().getDirection()

        score=0
        if min_distance <= 1:score+= 0
        else:
            if action == direction: score+= 2
            else:
                if nearfood > 0: score+= 3
                if score_difference > 0: score+= 4
        return score
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def MIN(state, Ghost_index, depth):
            LegalActions = state.getLegalActions(Ghost_index)
            if not LegalActions:
                return self.evaluationFunction(state)
            if Ghost_index == state.getNumAgents() - 1:
                return min(MAX(state.generateSuccessor(Ghost_index, action), depth) for action in LegalActions)
            else:
                return min(MIN(state.generateSuccessor(Ghost_index, action), Ghost_index + 1, depth) for action in
                           LegalActions)

        def MAX(state, depth):
            LegalActions = state.getLegalActions(0)
            if not LegalActions or depth == self.depth:
                return self.evaluationFunction(state)
            return max(MIN(state.generateSuccessor(0, action), 1, depth + 1) for action in LegalActions)

        MaxPayoff = float("-inf")
        for action in gameState.getLegalActions():
            payoff = MIN(gameState.generateSuccessor(0, action), 1, 1)
            if payoff > MaxPayoff:
                MaxPayoff = payoff
                BestAction = action

        return BestAction
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def MIN(state, Ghost_index, depth, alpha, beta):
            LegalActions = state.getLegalActions(Ghost_index)
            if not LegalActions:
                return self.evaluationFunction(state)
            payoff = float("inf")
            for action in LegalActions:
                if Ghost_index == state.getNumAgents() - 1:
                    New_payoff = MAX(state.generateSuccessor(Ghost_index, action), depth, alpha, beta)
                else:
                    New_payoff = MIN(state.generateSuccessor(Ghost_index, action), Ghost_index + 1, depth, alpha, beta)
                payoff = min(payoff, New_payoff)
                if payoff < alpha:
                    return payoff
                beta = min(beta, payoff)
            return payoff

        def MAX(state, depth, alpha, beta):
            LegalActions = state.getLegalActions(0)
            if not LegalActions or depth == self.depth:
                return self.evaluationFunction(state)
            payoff = float("-inf")
            if depth == 0:
                BestAction = LegalActions[0]
            for action in LegalActions:
                New_payoff = MIN(state.generateSuccessor(0, action), 1, depth + 1, alpha, beta)
                if New_payoff > payoff:
                    payoff = New_payoff
                    if depth == 0:
                        BestAction = action
                if payoff > beta:
                    return payoff
                alpha = max(alpha, payoff)
            if depth == 0:
                return BestAction
            return payoff

        BestAction = MAX(gameState, 0, float("-inf"), float("inf"))
        return BestAction
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def Expected_MIN(state, Ghost_index, depth):
            LegalActions = state.getLegalActions(Ghost_index)
            if not LegalActions:
                return self.evaluationFunction(state)
            P = 1/len(LegalActions)
            expected_minpayoff = 0
            for action in LegalActions:
                if Ghost_index == state.getNumAgents() - 1:
                    expected_minpayoff += MAX(state.generateSuccessor(Ghost_index, action), depth) * P
                else:
                    expected_minpayoff += Expected_MIN(state.generateSuccessor(Ghost_index, action), Ghost_index + 1, depth) * P
            return expected_minpayoff

        def MAX(state, depth):
            LegalActions = state.getLegalActions(0)
            if not LegalActions or depth == self.depth:
                return self.evaluationFunction(state)
            return max(Expected_MIN(state.generateSuccessor(0, action), 1, depth + 1) for action in LegalActions)

        MaxPayoff = float("-inf")
        for action in gameState.getLegalActions():
            payoff = Expected_MIN(gameState.generateSuccessor(0, action), 1, 1)
            if payoff > MaxPayoff:
                MaxPayoff = payoff
                BestAction = action

        return BestAction
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()

    ghostscore = 0
    for ghost in currentGameState.getGhostStates():
        GhostDistance = manhattanDistance(currentGameState.getPacmanPosition(), ghost.getPosition())
        if GhostDistance < 7:
            if ghost.scaredTimer > 0:
                ghostscore += pow(10-GhostDistance, 2)
            else:
                ghostscore -= pow(7-GhostDistance, 2)

    foodscore = 0
    for food in currentGameState.getFood():
        if 1/manhattanDistance(currentGameState.getPacmanPosition(), food) > foodscore:
            foodscore = 1/manhattanDistance(currentGameState.getPacmanPosition(), food)

    capsulescore = 0
    for capsule in currentGameState.getCapsules():
        if 100/manhattanDistance(currentGameState.getPacmanPosition(), capsule) > capsulescore:
            capsulescore = 10/manhattanDistance(currentGameState.getPacmanPosition(), capsule)
    
    return score + ghostscore + foodscore + capsulescore
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
