from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getDigitsFromString(self, str):
        """
        Helper method that takes in a string and parses through every character to
        see if there is a digit.

        Returns:
            Returns an int of all digits in order in the string
        """
        result = "";
        for d in str:
            if d.isdigit():
                result += d
        return int(result)


    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        #create an array to store final tuple
        result = []
        #create an array of arrays to store each pegs disks
        pegs = [[], [], []]
        #create an array of bindings to search for all disks' respective pegs
        reqs = [
        self.kb.kb_ask(Fact(['on', '?x', 'peg1'])),
        self.kb.kb_ask(Fact(['on', '?x', 'peg2'])),
        self.kb.kb_ask(Fact(['on', '?x', 'peg3'])),
        ]

        #for all three pegs...
        for x in range(3):
            #if there is some disks on that peg...
            if reqs[x]:
                if reqs[x].list_of_bindings:
                    #then loop through all of the disks
                    for bnd, fac in reqs[x].list_of_bindings:
                        for f in fac:
                            #add this disk onto the respective array in pegs, getting only the int value
                            pegs[x].append(self.getDigitsFromString(str(f.statement.terms[0])))

        #for all three pegs...
        for i in range(3):
            #store each peg's disks
            li = pegs[i]
            #if the peg has some disks...
            if li is not None:
                #sort the disks in ascending order
                li.sort()
            #append the tuple of sorted disks to result to create an array of tuples
            result.append(tuple(li))
        #now simply return the tuple of the array of tuples to get a tuple of tuples
        return tuple(result)



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        #get the disk that needs to be moved, first term in movable
        disktomove = str(movable_statement.terms[0])
        #get the peg that the disk is moving from, second term in movable
        oldpeg = str(movable_statement.terms[1])
        #get the peg that the disk to moving to, third term in movable
        newpeg = str(movable_statement.terms[2])
        #set variables to hold possible names of any disks that will be affected by this move
        #essentially, either a disk that the moved disk will be placed on top of OR...
        #a disk that was underneath the moved disk and will now be the top disk on peg
        newdiskontopofpegstack = ""
        disktoplaceon = ""

        #get all bindings for anything the movable disk is on top of...
        newdiskontopofpegstackreq = self.kb.kb_ask(Fact(['ontopof', disktomove, '?a']))
        #if there is some disk the movable disk is on top of...
        if newdiskontopofpegstackreq:
            if newdiskontopofpegstackreq.list_of_bindings:
                for bnda, faca in newdiskontopofpegstackreq.list_of_bindings:
                    for f in faca:
                        #set the newdiskontopofpegstack variable to this disk's name
                        newdiskontopofpegstack = str(f.statement.terms[1])

        #get all bindings for any disk that was on top of the new peg
        disktoplaceonreq = self.kb.kb_ask(Fact(['ontopofpegstack', '?a', newpeg]))
        #if there was a peg on the new peg to be moved to...
        if disktoplaceonreq:
            if disktoplaceonreq.list_of_bindings:
                for bndb, facb in disktoplaceonreq.list_of_bindings:
                    for f in facb:
                        #set the disktoplaceon variable to this disk's name
                        disktoplaceon = str(f.statement.terms[0])

        #if you move a disk, it is no longer on its old peg
        self.kb.kb_retract(Fact(['on', disktomove, oldpeg]))
        #if you move a disk and it had a disk underneath, it is no longer on top of the disk underneath
        if newdiskontopofpegstack != "":
            self.kb.kb_retract(Fact(['ontopof', disktomove, newdiskontopofpegstack]))
        #if you move a disk, then it is no longer on top of the old peg
        self.kb.kb_retract(Fact(['ontopofpegstack', disktomove, oldpeg]))
        #if you move a disk to a peg with another disk, then the other disk is no longer on top of its peg
        if disktoplaceon != "":
            self.kb.kb_retract(Fact(['ontopofpegstack', disktoplaceon, newpeg]))

        #if you move a disk, then you are on its new peg
        self.kb.kb_assert(Fact(['on', disktomove, newpeg]))
        #if you move a disk to a peg with another disk, then the other disk has this disk placed on top of itself
        if disktoplaceon != "":
            self.kb.kb_assert(Fact(['ontopof', disktomove, disktoplaceon]))
        #if you move a disk, it is now on top of a new peg
        self.kb.kb_assert(Fact(['ontopofpegstack', disktomove, newpeg]))
        #if you move a disk and it had a disk underneath, the other disk is now on top of its peg
        if newdiskontopofpegstack != "":
            self.kb.kb_assert(Fact(['ontopofpegstack', newdiskontopofpegstack, oldpeg]))

        #get all bindings for any disks on peg1
        oldpegreq = self.kb.kb_ask(Fact(['on', '?a', "peg1"]))
        if oldpegreq:
            if oldpegreq.list_of_bindings:
                pass
        #if no disks on peg1, then assert that it is empty
        else:
            self.kb.kb_assert(Fact(['isempty', "peg1"]))

        #get all bindings for any disks on peg2
        oldpegreq = self.kb.kb_ask(Fact(['on', '?a', "peg2"]))
        if oldpegreq:
            if oldpegreq.list_of_bindings:
                pass
        #if no disks on peg2, then assert that it is empty
        else:
            self.kb.kb_assert(Fact(['isempty', "peg2"]))

        #get all bindings for any disks on peg3
        oldpegreq = self.kb.kb_ask(Fact(['on', '?a', "peg3"]))
        if oldpegreq:
            if oldpegreq.list_of_bindings:
                pass
        #if no disks on peg3, then assert that it is empty
        else:
            self.kb.kb_assert(Fact(['isempty', "peg3"]))


        #get all bindings for any empty pegs
        emptyreq = self.kb.kb_ask(Fact(['isempty', '?a']))
        #if there is an empty peg...
        if emptyreq:
            if emptyreq.list_of_bindings:
                for bndc, facc in emptyreq.list_of_bindings:
                    for f in facc:
                        emptypegtest = f.statement.terms[0]
                        #then test it by asking to see if there are any disks on it
                        emptytestreq = self.kb.kb_ask(Fact(['on', '?a', emptypegtest]))
                        #if there are disks on a empty peg...
                        if emptytestreq:
                            if emptytestreq.list_of_bindings:
                                #that peg is no longer empty
                                self.kb.kb_retract(Fact(['isempty', emptypegtest]))



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getDigitsFromString(self, str):
        """
        Helper method that takes in a string and parses through every character to
        see if there is a digit.

        Returns:
            Returns an int of all digits in order in the string
        """
        result = "";
        for d in str:
            if d.isdigit():
                result += d
        return int(result)

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        #use a python dictionary to hold board coordinates of tiles
        board = {}
        #get the bindings for all XY coordinates of tiles
        tilesXY = self.kb.kb_ask(Fact(['XY', '?a' , '?x', '?y']))
        for bnd, fac in tilesXY.list_of_bindings:
            for f in fac:
                #get tile name, first term in fact's statement of XY
                tileName = str(f.statement.terms[0])
                #get coordinates from 2nd and 3rd terms of XY fact
                xCord = self.getDigitsFromString(str(f.statement.terms[1]))
                yCord = self.getDigitsFromString(str(f.statement.terms[2]))
                #if it's empty, then we use -1...
                if tileName == "empty":
                    tileNum = -1
                #otherwise, we are using the digit from our helper method
                else:
                    tileNum = self.getDigitsFromString(tileName)
                #use dictionary as a matrix to store each coordinate's tile
                board[xCord,yCord] = tileNum
        #return the matrix-like dictionary's contents in a tuple format
        return ((board[1,1],board[2,1],board[3,1]),(board[1,2],board[2,2],board[3,2]),(board[1,3],board[2,3],board[3,3]))


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        #get the name of the tile to move, is the first term of movable's fact
        tileToMove = movable_statement.terms[0]
        #get the tile's X
        initX = movable_statement.terms[1]
        #get the tile's Y
        initY = movable_statement.terms[2]
        #get the empty slot's X
        destX = movable_statement.terms[3]
        #get the empty slot's Y
        destY = movable_statement.terms[4]

        #if we are moving a tile, then remove XY coordinates of tile moved
        self.kb.kb_retract(Fact(['X',str(tileToMove),str(initX)]))
        self.kb.kb_retract(Fact(['Y',str(tileToMove),str(initY)]))
        #if we are moving a tile, then remove XY coordinates of the empty slot
        self.kb.kb_retract(Fact(['X','empty',str(destX)]))
        self.kb.kb_retract(Fact(['Y','empty',str(destY)]))

        #if we are moving a tile, then add XY coordinates of tile moved's destination
        self.kb.kb_assert(Fact(['X',str(tileToMove),str(destX)]))
        self.kb.kb_assert(Fact(['Y',str(tileToMove),str(destY)]))
        #if we are moving a tile, then add XY coordinates of new empty slot
        self.kb.kb_assert(Fact(['X','empty',str(initX)]))
        self.kb.kb_assert(Fact(['Y','empty',str(initY)]))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
