
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    stack = []
    steps = []
    count = 0

    def populateDFS(self):
        global stack
        global steps
        self.stack.append(self.currentState)
        while self.stack:
            current = self.stack.pop()
            key = current
            if not self.visited.get(key, False):
                self.visited[key] = True
                self.steps.append(current)

                if current.state == self.victoryCondition:
                    return

                if current.requiredMovable is not None:
                    self.gm.makeMove(current.requiredMovable)

                poss = self.gm.getMovables()
                for c in poss:
                    self.gm.makeMove(c)
                    child = GameState(self.gm.getGameState(), current.depth + 1, c)
                    if child.state == self.victoryCondition:
                        self.steps.append(child)
                        return
                    self.gm.reverseMove(c)
                    child.parent = current
                    keyChild = child
                    if not self.visited.get(keyChild, False):
                        self.stack.append(child)


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        global count
        global steps
        self.visited = {}
        if self.count == 0:
            self.populateDFS();
            #for s in self.steps:
                #print(s.state)
        self.count += 1
        print(self.count -1)
        if self.count >= len(self.steps):
            print("error: count too large")
            return False
        self.currentState = self.steps[self.count - 1]
        print(self.currentState.state)
        if self.currentState.state == self.victoryCondition:
            return True

        return False





class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
