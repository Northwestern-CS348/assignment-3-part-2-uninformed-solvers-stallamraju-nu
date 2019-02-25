
from solver import *
#import a queue
from collections import deque

class SolverDFS(UninformedSolver):
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
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState] = True
            return True

        self.visited[self.currentState] = True

        poss = self.gm.getMovables()

        for c in poss:
            self.gm.makeMove(c)
            child = GameState(self.gm.getGameState(), self.currentState.depth + 1, c)
            if not self.visited.get(child, False):
                child.parent = self.currentState
                self.currentState.children.append(child)
            self.gm.reverseMove(c)

        if self.currentState.nextChildToVisit < len(self.currentState.children):
            self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)
            self.currentState.nextChildToVisit += 1
            self.currentState = self.currentState.children[self.currentState.nextChildToVisit-1]
            return False

        #no children
        p = self.currentState.parent
        c = self.currentState

        while p is not None and p.nextChildToVisit >= len(p.children):
            c = p
            self.gm.reverseMove(c.requiredMovable)
            p = p.parent

        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    q = deque([])
    count = 0

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
        global q
        global count

        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState] = True
            self.q.clear()
            return True

        self.visited[self.currentState] = True

        poss = self.gm.getMovables()

        #print(self.count)
        #self.count += 1
        #print(self.currentState.state)

        for c in poss:
            self.gm.makeMove(c)
            child = GameState(self.gm.getGameState(), self.currentState.depth + 1, c)
            if not self.visited.get(child, False):
                child.parent = self.currentState
                self.currentState.children.append(child)
                self.q.append(child)
            self.gm.reverseMove(c)

        popped = self.q.popleft()
        while self.visited.get(popped, False):
            popped = self.q.popleft()

        c = self.currentState
        while c.parent is not None:
            self.gm.reverseMove(c.requiredMovable)
            c = c.parent

        #print(self.gm.getGameState())

        p = popped
        steps = []
        while p is not None:
            steps.append(p)
            p = p.parent

        #print("start")
        #for s in steps:
            #print(s.state)
        if steps:
            steps.pop()
        #print("end")
        #print("start")
        #print(self.gm.getGameState())
        for a in reversed(steps):
            self.gm.makeMove(a.requiredMovable)
            #print(self.gm.getGameState())
        #print("end")

        #print("what we want")
        #print(popped.state)
        #print("what we have")
        #print(self.gm.getGameState())

        self.currentState = popped
        #print("start")
        #print(self.gm.getGameState())
        #print(self.currentState.state)
        #print("end")
        return False
