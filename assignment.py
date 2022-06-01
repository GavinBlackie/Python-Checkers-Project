#-----------------------------------------------------------------------------
# Name:        Checkers!
# Purpose:     A program that provides an enjoyable experience of the game checkers for the user(s)
#
# Author:      Gavin B.
# Created:     04-May-2022
# Updated:     01-Jun-2022
#-----------------------------------------------------------------------------
#I think this project deserves a level 4 because ...
#
#  - The program does not have any major errors, I am confident that there are none after constant testing of the program
#  - The user input is fairly simplistic, the user uses the mouse to click things, four keys chosen to make a diagonal
#    layout in order to move pieces as well as the escape button to pause/return to start menu
#  - Diffrent variable types are used throughout the program as well as lots of conditional structures, ex. for loops, if statements
#  - Custom functions and functions in general are used throughout the program
#  - Lists are extensively used in the program
#  - Program both reads and writes to multiple files, it reads the previous game data and writes the current data in order to create
#    the continuing and save features
#  - There is a laid out start, game and end screens shown by the "If programState == ___:" statments
#  - Loads of comments are present throughout the program as well as the proper documentation for functions
#  - The code is efficient in my opinion but still could be improved for what it does, ex. the movement functions save about 4 times their
#    respective line lengths each, however I see potential to combine them into one big function that controls all movements in the game
#  - The input and output of the program is sanitized, if you mash the keyboard in a game it will not crash as it will only do what it is
#    supposed to when given the correct input
#  - Program is modular, a great deal of it is divided across multiple functions that are called upon in their respective programStates
#
#Features Added:
#
#   - Interactable and moveable pieces for both black and red teams
#   - Jumping and killing, pieces will jump over the opposite teams pieces if the conditions are right
#   - King pieces: when a piece on a team reaches the end of the board, they are granted the ability to move backwards as well as forwards
#   - Functioning main menu and help menu that the player can go back and forth from without restarting game
#   - Pausing, continuing and game saving as games can be saved and continued inside the program as well as outside the program, when a user stops then
#     starts the program they can start from where they left off from or even start a new game altogether
#-----------------------------------------------------------------------------

import pygame
import math

def distFromPoints(point1, point2): # Function from python lesson on collision detection, used for circle collision detection in relation to the pieces
    '''
    This function calculationes the distance between two points given by a set of tuples (x1,y1) and (x2,y2)
    
    Parameters
    ----------
    point1 : float
        The first point to compare
    point2 : float
        The second point to compare
        
    Returns
    float
        The distance between the two points
    '''
    distance = math.sqrt( ((point2[0]-point1[0])**2)+((point2[1]-point1[1])**2) )
    
    return distance

def main():
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 720   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower
    
    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
    
                                    #------------Variables------------
    
    # Various Game State Variables
    programState = 'Start Menu'
    previousState = ''
    
    #Colours:
    white = (255, 255, 255)
    grey = (140, 140, 140)
    black = (0, 0, 0)
    red = (255, 0, 0)
    yellow = (229, 255, 0)
    green = (0, 255, 0)
    goldBrown = (155, 114, 0)
    
    #Tile Variables
    tilePos = [72, 72]
    tileWidth = 72
    tileHeight = 72
    tileShift = False
    
    #Fonts
    titleFont = pygame.font.SysFont("Times New Roman", 65)
    buttonFont = pygame.font.SysFont("Times New Roman", 26)
    
    # Board
    
    #             X0          X1          X2          X3          X4          X5          X6          X7
    board0 = [(108, 108), (180, 108), (252, 108), (324, 108), (396, 108), (468, 108), (540, 108), (612, 108)] # Y0
    board1 = [(108, 180), (180, 180), (252, 180), (324, 180), (396, 180), (468, 180), (540, 180), (612, 180)] # Y1
    board2 = [(108, 252), (180, 252), (252, 252), (324, 252), (396, 252), (468, 252), (540, 252), (612, 252)] # Y2
    board3 = [(108, 324), (180, 324), (252, 324), (324, 324), (396, 324), (468, 324), (540, 324), (612, 324)] # Y3
    board4 = [(108, 396), (180, 396), (252, 396), (324, 396), (396, 396), (468, 396), (540, 396), (612, 396)] # Y4
    board5 = [(108, 468), (180, 468), (252, 468), (324, 468), (396, 468), (468, 468), (540, 468), (612, 468)] # Y5
    board6 = [(108, 540), (180, 540), (252, 540), (324, 540), (396, 540), (468, 540), (540, 540), (612, 540)] # Y6
    board7 = [(108, 612), (180, 612), (252, 612), (324, 612), (396, 612), (468, 612), (540, 612), (612, 612)] # Y7
    
    board = [ board0, board1, board2, board3, board4, board5, board6, board7] # List of lists, the board as a list
    
    # Piece Variables
    
    # Base Red Piece values
    redPiece = [ [0, 0,], [2, 0], [4, 0], [6, 0], [1, 1], [3, 1], [5, 1], [7, 1] ] # Red piece coordinates
    redStatus = ['Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive'] # Red piece alive/dead list
    redKing = ['Notking', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing'] # Red piece king list
    redColour = [red, red, red, red, red, red, red, red] # Colours of the red pieces (For piece highlighting)
    
    # Base Black Piece values
    blackPiece = [ [0, 6], [2, 6], [4, 6], [6, 6], [1, 7], [3, 7], [5, 7], [7, 7] ] # Black piece coordinates
    blackStatus = ['Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive'] # Black piece alive/dead list
    blackKing = ['Notking', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing'] # Black piece king list
    blackColour = [black, black, black, black, black, black, black, black] # Colours of the black pieces (For piece highlighting)
    
    pieceRadius = 30 # Radius of the pieces
    pieceChosen = False # Statement on if a piece has been chosen or not
    
    # Other Variables
    
    readingFiles = True # True-false statement to control the amount of tiles the files are read in the start menu (should be only once)
    helpMenu = pygame.image.load('images/help_menu.png') # the variable of the png for the help menu
    gameWinner = '' # String to be used when a winner is declared on the end screen
    turnTextPos = (540, 670) # Tuple of where the turn show text is when it is either player 1 or player 2 turn
    
                                     #--------------------------------
    
    
    #--------------------Functions--------------------
    
    #---------------Left Side Movement---------------
    def leftMove(upDown, teamPiece, teamStatus, enemyPiece, enemyStatus, inputMethod):
        '''
        Checks all the conditions for a piece to move left or jump left, jumps or moves left if conditions fullfilled.
        
        Function that takes in a bunch of values specific to the conditions of a left movement in a checker game. First,
        it takes the inputMethod and checks if the player inputed the same method, then it checks if the place they are
        trying to move exists, otherwise do nothing. Then it goes through all piece indexes that are "Alive" and checks
        if they are in the way or not, then it checks it a piece is in a jumping range. If the piece that was beside the
        desired left movement was an enemy, it jumps, otherwise nothing happens. In the case that another team piece was
        in the way of jumping it will not jump. It will only allow a jump left if there is no alive piece on any team in
        the way and that the piece in the way is on the opposing team. Additionally a regular movement when there is no
        alive piece in the way will also pass through the code and ignore the jumping aspect.
        
        Parameters
        ----------
        upDown : int
            directional variable, ment to only be a 1 or a -1 to determine which way the piece wants to move vertically
        teamPiece : int
            list of 8 pair ints of the x and y indexes, on the board, for pieces on the team that is trying to move
        teamStatus : str
            list of 8 strings that represent the dead/alive status of the pieces whose are on the team whom is trying to move a piece
        enemyPiece : int
            list of 8 pair ints of the x and y indexes, on the board, for pieces on the opposing team
        enemyStatus : str
            list of 8 strings that represent the dead/alive status of the enemy teams pieces
        inputMethod : str
            the string/unicode variable to be checked by the function
            
        Returns
        -------
        boolean
            true/false statement on whether the function allowed the piece to move.
        
        '''
        if ev.unicode == inputMethod: # Check for input
            if teamPiece[selectedIndex][0]-1 >= 0: # If the tile to the left is not off the screen
                canMove = True
                farSideBlocked = False
                enemyPieceInWay = False
                
                for i in range(0, 8, 1): # Do this 8 times, number of piece indexes for red and black pieces
                    if teamStatus[i] == 'Alive':
                        if teamPiece[i][0] == (teamPiece[selectedIndex][0]-1) and teamPiece[i][1] == (teamPiece[selectedIndex][1]+upDown): # Check for a black piece to the top left
                            canMove = False
                        
                    if enemyStatus[i] == 'Alive':
                        if enemyPiece[i][0] == (teamPiece[selectedIndex][0]-1) and enemyPiece[i][1] == (teamPiece[selectedIndex][1]+upDown):# Check for a red piece to the top left
                            enemyPieceInWay = True
                            enemyIndex = i #Temp record the index of the enemy piece (in the case it needs to be killed)
                            
                            for count in range(0, 8, 1): # Do this 8 times, number of pieces on each side - check if there is any team's piece in the way of a jump and is alive
                                if enemyPiece[count][0] == (teamPiece[selectedIndex][0]-2) and enemyPiece[count][1] == (teamPiece[selectedIndex][1]+(2*upDown)) and enemyStatus[count] == 'Alive':
                                    farSideBlocked = True
                                if teamPiece[count][0] == (teamPiece[selectedIndex][0]-2) and teamPiece[count][1] == (teamPiece[selectedIndex][1]+(2*upDown)) and teamStatus[count] == 'Alive':
                                    farSideBlocked = True
                            
                            canMove = False
                            
                if farSideBlocked == False and enemyPieceInWay == True: # If the jump is not blocked and an enemy is in the way
                    if (teamPiece[selectedIndex][0]-2) != -1:
                        if (teamPiece[selectedIndex][1]+(2*upDown)) != -1 and (teamPiece[selectedIndex][1]+(2*upDown)) != 8:
                            teamPiece[selectedIndex][1] += 2*upDown
                            teamPiece[selectedIndex][0] -= 2
                            enemyStatus[enemyIndex] = 'Dead' # Kill the enemy piece
                            return True
                        else: # The piece cannot jump, reset
                            return False 
                if canMove == True: # If the piece can move (and has not jumped), move one space
                    teamPiece[selectedIndex][1] += upDown
                    teamPiece[selectedIndex][0] -= 1
                    return True 
        return False
           
    #---------------Right Side Movement--------------
    def rightMove(upDown, teamPiece, teamStatus, enemyPiece, enemyStatus, inputMethod):
        '''
        
        Checks all the conditions for a piece to move right or jump right, jumps or moves right if conditions fullfilled.
        
        Function that takes in a bunch of values specific to the conditions of a right movement in a checker game. First,
        it takes the inputMethod and checks if the player inputed the same method, then it checks if the place they are
        trying to move exists, otherwise do nothing. Then it goes through all piece indexes that are "Alive" and checks
        if they are in the way or not, then it checks it a piece is in a jumping range. If the piece that was beside the
        desired right movement was an enemy, it jumps, otherwise nothing happens. In the case that another team piece was
        in the way of jumping it will not jump. It will only allow a jump right if there is no alive piece on any team in
        the way and that the piece in the way is on the opposing team. Additionally a regular movement when there is no
        alive piece in the way will also pass through the code and ignore the jumping aspect.
        
        Parameters
        ----------
        upDown : int
            directional variable, ment to only be a 1 or a -1 to determine which way the piece wants to move vertically
        teamPiece : int
            list of 8 pair ints of the x and y indexes, on the board, for pieces on the team that is trying to move
        teamStatus : str
            list of 8 strings that represent the dead/alive status of the pieces whose are on the team whom is trying to move a piece
        enemyPiece : int
            list of 8 pair ints of the x and y indexes, on the board, for pieces on the opposing team
        enemyStatus : str
            list of 8 strings that represent the dead/alive status of the enemy teams pieces
        inputMethod : str
            the string/unicode variable to be checked by the function
            
        Returns
        -------
        boolean
            true/false statement on whether the function allowed the piece to move.
        
        '''             
        if ev.unicode == inputMethod: # Check for input
            if teamPiece[selectedIndex][0]+1 <= 7: # If the tile to the right is not off the screen
                canMove = True
                farSideBlocked = False
                enemyPieceInWay = False
                
                for i in range(0, 8, 1): # Do this 8 times, number of piece indexes for red and black pieces
                    if teamStatus[i] == 'Alive':
                        if teamPiece[i][0] == (teamPiece[selectedIndex][0]+1) and teamPiece[i][1] == (teamPiece[selectedIndex][1]+upDown): # Check for a team piece to the top right  
                            canMove = False
                    
                    if enemyStatus[i] == 'Alive':
                        if enemyPiece[i][0] == (teamPiece[selectedIndex][0]+1) and enemyPiece[i][1] == (teamPiece[selectedIndex][1]+upDown):# Check for a enemy piece to the top right
                            enemyPieceInWay = True
                            enemyIndex = i #Temp record the index of the enemy piece (in the case it needs to be killed)
                            
                            for count in range(0, 8, 1): # Do this 8 times, number of pieces on each side - check if there is any team's piece in the way of a jump and is alive
                                if enemyPiece[count][0] == (teamPiece[selectedIndex][0]+2) and enemyPiece[count][1] == (teamPiece[selectedIndex][1]+(2*upDown)) and enemyStatus[count] == 'Alive':
                                    farSideBlocked = True
                                if teamPiece[count][0] == (teamPiece[selectedIndex][0]+2) and teamPiece[count][1] == (teamPiece[selectedIndex][1]+(2*upDown)) and teamStatus[count] == 'Alive':
                                    farSideBlocked = True
                                
                            canMove = False
                        
                if farSideBlocked == False and enemyPieceInWay == True:
                    if (teamPiece[selectedIndex][0]+2) != 8:
                        if (teamPiece[selectedIndex][1]+(2*upDown)) != -1 and (teamPiece[selectedIndex][1]+(2*upDown)) != 8:
                            teamPiece[selectedIndex][1] += 2*upDown
                            teamPiece[selectedIndex][0] += 2
                            enemyStatus[enemyIndex] = 'Dead' # Kill the enemy piece
                            return True
                        else: # The piece cannot jump, reset
                            return False 
                if canMove == True: # If the piece can move (and has not jumped), move one space
                    teamPiece[selectedIndex][1] += upDown
                    teamPiece[selectedIndex][0] += 1
                    return True
        return False
    
    def deadCheck():
        '''
        If a player's pieces are dead, return a str value to tell which player died.
        
        Simple function that checks if all the black pieces are dead and
        it will also check if the red pieces are dead. Then it will return
        the correct string for the rest of the code to work out who wins.
        
        Parameters
        ----------
        None
        
        
        Returns
        -------
        str
            statement on which player's pieces are dead
        '''
        if blackStatus == ['Dead', 'Dead', 'Dead', 'Dead', 'Dead', 'Dead', 'Dead', 'Dead']:
            return 'Player 1 is dead'
        elif redStatus == ['Dead', 'Dead', 'Dead', 'Dead', 'Dead', 'Dead', 'Dead', 'Dead']:
            return 'Player 2 is dead'
        return None
    
    def kingCheck():
        '''
        Basic function that detects if a black or red piece is at the end of the screen,
        if so it changes their king variable to 'King' to identify they are now a king
        piece for the movement code to use.
        
        Parameters
        ----------
        None
        
        
        Returns
        -------
        None
        
        '''
        for i in range(0, 8, 1):
            if blackPiece[i][1] <= 0:
                blackKing[i] = 'King'
            if redPiece[i][1] >= 7:
                redKing[i] = 'King'
    
    def drawKing(teamPiece, inputIndex):
        '''
        Draws the aesthetics of the king pieces using the inputed info on that piece's team as well as the
        index of the piece that needs the crown to be drawn ontop of.
        
        Parameters
        ----------
        teamPiece : [list, list, list, list, list, list, list, list]
            list of lists that contain the pair of numbers corresponding to the set of pieces on the specified team
        inputIndex : int
            the index of the piece to have a crown drawn upon them
            
        
        Returns
        -------
        None
                    
        '''
        # Draw commands use triple list [][][] to find the exact tuple in the board list in order to change the x and y of the rects individually
        pygame.draw.rect(mainSurface, yellow, ( board[teamPiece[inputIndex][1]][teamPiece[inputIndex][0]] [0]-10, board[teamPiece[inputIndex][1]][teamPiece[inputIndex][0]] [1], 20, 5) )
        pygame.draw.rect(mainSurface, yellow, ( board[teamPiece[inputIndex][1]][teamPiece[inputIndex][0]] [0]-10, board[teamPiece[inputIndex][1]][teamPiece[inputIndex][0]] [1]-5, 4, 5) )
        pygame.draw.rect(mainSurface, yellow, ( board[teamPiece[inputIndex][1]][teamPiece[inputIndex][0]] [0]-2, board[teamPiece[inputIndex][1]][teamPiece[inputIndex][0]] [1]-5, 4, 5) )
        pygame.draw.rect(mainSurface, yellow, ( board[teamPiece[inputIndex][1]][teamPiece[inputIndex][0]] [0]+6, board[teamPiece[inputIndex][1]][teamPiece[inputIndex][0]] [1]-5, 4, 5) )
        
    def drawPieces():
        '''
        Function that draws the pieces and their details.
        
        Runs a for loop eight times, the number of pieces on each side, then checks if
        a piece is alive, if so it draws that piece with that index on that team. In the
        case that the corresponding index also has the characteristic of "King" in their
        respective king variable list, it draws the crown using the drawKing function.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        
        '''
        
        for i in range(0, 8, 1): # Run draw loop 8 times, number of pieces on each side
            if redStatus[i] == 'Alive': # Check if the piece is alive
                pygame.draw.circle(mainSurface, redColour[i], board[redPiece[i][1]][redPiece[i][0]], pieceRadius)
                if redKing[i] == 'King': # Draw king details if piece has 'King' characteristic
                    drawKing(redPiece, i)
            if blackStatus[i] == 'Alive': # Check if the piece is alive
                pygame.draw.circle(mainSurface, blackColour[i], board[blackPiece[i][1]][blackPiece[i][0]], pieceRadius)
                if blackKing[i] == 'King': # Draw king details if piece has 'King' characteristic
                    drawKing(blackPiece, i)
        
    def readInfo():
        '''
        Reads the existing files and replaces the respective variables with the ones
        written in the files.
        
        Function that resets the variables that are going to be replaced. Then reads them
        in the right format. Most use a variable called "coordinateGrouper" to help format
        the data in the right way as redPiece and blackPiece require lists inside of lists.
        The "coordinateGrouper" goes into play here as it groups up the data in small lists
        of two, puts them into the new variable and then resets itself for the next pair of
        numbers to be read. The variables that do not need this specific altering instead
        read each line individually and places them inside the code, exeption being the
        previousState as it only needs one line to read.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        
        '''
            
        # Reset the variables to be read into
        redPiece = []
        redStatus = []
        redKing = []
        blackPiece = []
        blackStatus = []
        blackKing = []
        
        
        #-Coordinate Reading-
        # Read the red coordinates
        coordinateGrouper = []
        redCoordFile = open('last_game_info/redPieceCoordinates.txt', 'r')
        while True: # Forever while loop until there is nothing left to read in file (see the if len(theLine) statement)
            theLine = redCoordFile.readline()
            theLine = theLine.strip('\n')
            if len(theLine) == 0: # If there is nothing on the currently red line, add the last read line and break
                redPiece.append(coordinateGrouper)
                break
            
            theLine = int(theLine) # Redefine as an int variable (so it can be used in the game)
            if len(coordinateGrouper) >= 2: # Check if the coordinate grouper does not include 2 variables, if so errase/reset it
                redPiece.append(coordinateGrouper) # Add the list to the redPiece list (should be a list of lists that comprise of two integers)
                coordinateGrouper = []
                
            coordinateGrouper.append(theLine) # Add the data to the coordinateGrouper list
        redCoordFile.close()
        # Read the black coordinates
        coordinateGrouper = []
        blackCoordFile = open('last_game_info/blackPieceCoordinates.txt', 'r')
        while True: # Forever while loop until there is nothing left to read in file (see the if len(theLine) statement)
            theLine = blackCoordFile.readline()
            theLine = theLine.strip('\n')
            if len(theLine) == 0: # If there is nothing on the currently red line, add the last read line and break
                blackPiece.append(coordinateGrouper)
                break
            
            theLine = int(theLine) # Redefine as an int variable (so it can be used in the game)
            if len(coordinateGrouper) >= 2: # Check if the coordinate grouper does not include 2 variables, if so errase/reset it
                blackPiece.append(coordinateGrouper) # Add the list to the redPiece list (should be a list of lists that comprise of two integers)
                coordinateGrouper = []
                
            coordinateGrouper.append(theLine) # Add the data to the coordinateGrouper list
        blackCoordFile.close()
        
        
        #-Status Reading-
        # Read the red status
        redStatFile = open('last_game_info/redPieceStatus.txt', 'r')
        while True: # Forever while loop until there is nothing left to read in file
            theLine = redStatFile.readline()
            theLine = theLine.strip('\n')
            if len(theLine) == 0: #If there is nothing on the line, break
                break
            
            redStatus.append(theLine) # Add the line to the redStatus
        redStatFile.close()
        # Read the black status
        blackStatFile = open('last_game_info/blackPieceStatus.txt', 'r')
        while True: # Forever while loop until there is nothing left to read in file
            theLine = blackStatFile.readline()
            theLine = theLine.strip('\n')
            if len(theLine) == 0: #If there is nothing on the line, break
                break
            
            blackStatus.append(theLine) # Add the line to the blackStatus
        blackStatFile.close()
        
        #-King Reading-
        # Read the red king values
        redKingFile = open('last_game_info/redKing.txt', 'r')
        while True: # Forever while loop until there is nothing left to read in file
            theLine = redKingFile.readline()
            theLine = theLine.strip('\n')
            if len(theLine) == 0: #If there is nothing on the line, break
                break
            
            redKing.append(theLine) # Add the line to redKing
        redKingFile.close()
        
        # Read the black king values
        blackKingFile = open('last_game_info/blackKing.txt', 'r')
        while True: # Forever while loop until there is nothing left to read in file
            theLine = blackKingFile.readline()
            theLine = theLine.strip('\n')
            if len(theLine) == 0: #If there is nothing on the line, break
                break
            
            blackKing.append(theLine) # Add the line to blackKing
        blackKingFile.close()
        
        #-Other File Reading-
        # Read the previous program state
        prevStateFile = open('last_game_info/previousGameState.txt', 'r')
        previousState = prevStateFile.readline()
        prevStateFile.close()
        
        return blackPiece, redPiece, blackStatus, redStatus, blackKing, redKing, previousState
    
    def writeInfo():
        '''
        Function that writes the last stats known to the game into their respective
        text files.
        
        Function that overwrites the last known values of the black coords, red coords,
        the red status, the black status and the previous program state. Use a for loop
        that runs for eight times for all writes that require eight different pairs of
        numbers (with the exception of the previous program state).
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        # Open the red files
        redCoordFile = open('last_game_info/redPieceCoordinates.txt', 'w')
        redStatFile = open('last_game_info/redPieceStatus.txt', 'w')
        redKingFile = open('last_game_info/redKing.txt', 'w')
        # Open the black files
        blackCoordFile = open('last_game_info/blackPieceCoordinates.txt', 'w')
        blackStatFile = open('last_game_info/blackPieceStatus.txt', 'w')
        blackKingFile = open('last_game_info/blackKing.txt', 'w')
        
        for i in range(0, 8, 1):
            redCoordFile.write(f'{redPiece[i][0]}\n{redPiece[i][1]}\n')
            redStatFile.write(f'{redStatus[i]}\n')
            redKingFile.write(f'{redKing[i]}\n')
            blackCoordFile.write(f'{blackPiece[i][0]}\n{blackPiece[i][1]}\n')
            blackStatFile.write(f'{blackStatus[i]}\n')
            blackKingFile.write(f'{blackKing[i]}\n')
        
        # Close the red files
        redCoordFile.close()
        redStatFile.close()
        redKingFile.close()
        # Close the black Files
        blackCoordFile.close()
        blackStatFile.close()
        blackKingFile.close()
        # Write reset version of black king
        
        # Write reset version of programState
        prevStateFile = open('last_game_info/previousGameState.txt', 'w')
        prevStateFile.write(previousState)
        prevStateFile.close()
    
    #--------------------------------------
    
    
    #----Object Classes----
    
    class button(): #Class object for tiles and buttons
        def __init__(self, inputColour, inputRect):
            '''
            Initializes the button and its variables for the program to draw from.
            
            Parameters
            ----------
            inputColour : (float, float, float)
                the inputed colour values for the button
            inputRect : [int, int, int, int]
                list of ints to identify the rectangle of the button
            
            Returns
            -------
            None
            
            '''
            self.rect = inputRect
            self.colour = inputColour
            
        def draw(self, inputSurface):
            '''
            Basic function that draws a singular tile on the surface given
            
            Parameters
            ----------
            inputSurface : (int, int, int)
                the surface at which the tile is drawn
                
            Returns
            -------
            None
            
            '''
            pygame.draw.rect(inputSurface, self.colour, self.rect)
            
        #Collide function, checks wheter or not the input point is within the button's boundaries (Function from my mini-game assignment)
        def buttonCollidePoint(self, inPnt):
            '''
            Function that returns True or False depending on whether or not the if statements are fullfilled.
              
            Takes the inPnt parameter, if it is within the boundaries of the button
            class's variables, checks if there is a mouse input as well as if it was
            the left click on the mouse. Then returns True if so (pressing button),
            else return False (not pressing button).


            Parameters
            ----------
            inPnt : int
                positional list of X & Y values used to be checked in if statement
              
            Returns
            -------
            boolean
                the statement regarding if the button was clicked or not
                
            '''
            if inPnt[0] > self.rect[0] and inPnt[0] < self.rect[0]+self.rect[2] and inPnt[1] < self.rect[1]+self.rect[3] and inPnt[1] > self.rect[1]:#Is the inpt colliding with button?
                if ev.type == pygame.MOUSEBUTTONDOWN: #Is there a mouse event?
                    if ev.button == 1: # If the left mouse is clicked, return true
                        return True
            return None
            
    
    class tile(): #Class object for tiles and buttons
        def __init__(self, inputColour, inputRect):
            '''
            Initializes the tile and its variables for the program to draw from.
            
            Parameters
            ----------
            inputColour : (float, float, float)
                the inputed colour values for the button
            inputRect : [int, int, int, int]
                list of ints to identify the rectangle of the button
            
            Returns
            -------
            None
            '''
            self.rect = inputRect
            self.colour = inputColour
        
        def drawTile(self, inputSurface):
            '''
            Basic function that draws a singular tile on the surface given
            
            Parameters
            ----------
            inputSurface : (int, int, int)
                the surface at which the tile is drawn
                
            Returns
            -------
            None
            '''
            pygame.draw.rect(inputSurface, self.colour, self.rect)
            
        
    #------Object Definitions (Initializations)------
    
    #--Buttons--
    
    newGameButton = button(green, [130, 440, 460, 60])
    continueGameButton = button(goldBrown, [160, 350, 400, 50])
    helpButton = button(yellow, [230, 525, 260, 50])
    exitButton = button(red, [290, 600, 140, 30])
    helpExit = button(red, [580, 650, 120, 40])
    pauseContinue = button(goldBrown, [160, 350, 400, 50])
    pauseMainMenu = button(red, [160, 425, 400, 50])
    endBackButton = button(red, [180, 440, 360, 60])
    
    #--Tile Loading--
    
    tiles = [] # List of tiles/tile information for the program to draw from

    for count in range(0, 8, 1):#For loop that repeats 8 times, the number of rows
        for count in range(0, 4, 1): #For loop that repeats 4 times, the number of columns
            tiles.append(tile( grey, [tilePos[0], tilePos[1], tileWidth, tileHeight]))
            tilePos[0] += tileWidth*2
        
        tilePos[1] += tileHeight # Add the y for the next line of tiles
        tilePos[0] -= tileWidth*8 # Decrease the x of the tiles by 8 times the width of one tile (the length of the board)
        tileShift = not tileShift # Alternating True/False statement
        #If & Elif statements make checker grid possible by changing the tilePos
        if tileShift == True:
            tilePos[0] += 72
        elif tileShift == False:
            tilePos[0] -= 72
            
    
    while True:
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
        
        mousePos = pygame.mouse.get_pos()#Mouse position for buttons
        
        if programState == 'Start Menu':
            # Update your game objects and data structures here...
            
            #---Reading Files---
            if readingFiles == True: # If statement that runs only once, declares variables to be set to the ones retunred in the readInfo function (with their respective indexes)
                blackPiece = readInfo()[0]
                redPiece = readInfo()[1]
                blackStatus = readInfo()[2]
                redStatus = readInfo()[3]
                blackKing = readInfo()[4]
                redKing = readInfo()[5]
                previousState = readInfo()[6]
                readingFiles = False # Stop this if statement from running over and over again in the menu to prevent lag
            #-------------------
                
            # Render Texts 
            renderedTitle = titleFont.render('Checkers!', True, white)
            renderedContinueGame = buttonFont.render('Continue Previous Game', True, black)
            renderedNew = buttonFont.render('New Game', True, black)
            renderedHelp = buttonFont.render('Help & Instructions', True, black)
            renderedExit = buttonFont.render('Exit', True, black)
            
            if continueGameButton.buttonCollidePoint(mousePos) == True: # Check if the continue game button has been pressed (will start with the newly read variables)
                programState = previousState
                
            elif newGameButton.buttonCollidePoint(mousePos) == True: # Check if the new game button has been pressed (will reset the newly read variables)
                redPiece = [ [0, 0,], [2, 0], [4, 0], [6, 0], [1, 1], [3, 1], [5, 1], [7, 1] ]
                redStatus = [ 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive']
                redKing = ['Notking', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing']
                redColour = [red, red, red, red, red, red, red, red]
                blackPiece = [ [0, 6], [2, 6], [4, 6], [6, 6], [1, 7], [3, 7], [5, 7], [7, 7] ]
                blackStatus = [ 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive']
                blackKing = ['Notking', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing']
                blackColour = [black, black, black, black, black, black, black, black]
                programState = 'Player 1 Turn'
                
            elif helpButton.buttonCollidePoint(mousePos) == True: # Check if the help button has been pressed, if so go to the help menu
                programState = 'Help Menu'
                
            elif exitButton.buttonCollidePoint(mousePos) == True: # If the Exit button has been pressed, save info (more as a precaution) and exit
                writeInfo()
                break
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            # Draw buttons
            newGameButton.draw(mainSurface)
            continueGameButton.draw(mainSurface)
            helpButton.draw(mainSurface)
            exitButton.draw(mainSurface)
            
            # Draw texts
            mainSurface.blit(renderedTitle, (230, 100))
            mainSurface.blit(renderedContinueGame, (235, 360))
            mainSurface.blit(renderedNew, (300, 455))
            mainSurface.blit(renderedHelp, (260, 535))
            mainSurface.blit(renderedExit, (340, 600))
            
            
        elif programState == 'Help Menu':
            # Update your game objects and data structures here...
            
            # Render texts
            renderedHelpTitle = titleFont.render('Help & How to Play', True, yellow)
            renderedBack = buttonFont.render('Back', True, black)
            
            if helpExit.buttonCollidePoint(mousePos) == True:
                programState = 'Start Menu'
                readingFiles = True
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            # Draw back button
            helpExit.draw(mainSurface)
            
            # Draw texts
            mainSurface.blit(renderedHelpTitle, (100, 100))
            mainSurface.blit(renderedBack, (615, 655))
            
            mainSurface.blit(helpMenu, (80, 210)) # Draw the help menu png
        
        elif programState == 'Pause Menu':
            # Update your game objects and data structures here...
            
            # Render texts
            renderedPauseTitle = titleFont.render('Paused', True, white)
            renderedResume = buttonFont.render('Resume Current Game', True, black)
            renderedSaveQuit = buttonFont.render('Save & Quit to Menu', True, black)
            
            if pauseContinue.buttonCollidePoint(mousePos) == True: # Check if the contine game button has been pressed, if so return to the previous programState
                programState = previousState
            elif pauseMainMenu.buttonCollidePoint(mousePos) == True: # Check if the main menu button has been pressed, if so return to the start menu and write down the last game stats
                programState = 'Start Menu'
                readingFiles = True
                
                #-File Writing-
                writeInfo()
                
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            # Draw buttons
            pauseContinue.draw(mainSurface)
            pauseMainMenu.draw(mainSurface)
            
            # Draw texts
            mainSurface.blit(renderedPauseTitle, (260, 100))
            mainSurface.blit(renderedResume, (250, 360))
            mainSurface.blit(renderedSaveQuit, (250, 435))
            
            
        elif programState == 'Player 1 Turn':
            # Update your game objects and data structures here...
            
            kingCheck() # Check if any pieces are eligible to be a king piece
            
            if deadCheck() == 'Player 1 is dead': # Check if player 1's pieces are dead, end game if so
                programState = 'End Screen'
                gameWinner = '2'
            elif deadCheck() == 'Player 2 is dead': # Check if player 2's pieces are dead, end game if so
                programState = 'End Screen'
                gameWinner = '1'
            
            renderedTurnShow = buttonFont.render("Player 1's Turn", True, white)
            
            if ev.type == pygame.KEYDOWN: # If a key was pressed
                if ev.scancode == 41: # If the key was the esc key, record the programState and go to pause menu
                    previousState = programState
                    programState = 'Pause Menu'
            
            if ev.type == pygame.MOUSEBUTTONDOWN: # Is there a mouse event
                if pieceChosen == False: # If no piece has been selected
                    for i in range(0, len(blackPiece), 1): # Check all black piece indexes
                        if distFromPoints(board[blackPiece[i][1]][blackPiece[i][0]], mousePos) < pieceRadius: # If there is a collision between the mouse and a black piece
                            if blackStatus[i] == 'Alive': # Check if the piece is alive
                                pieceChosen = True
                                selectedIndex = i # Temp variable to hold the index of the piece in the piece list
                                blackColour[selectedIndex] = yellow
            
            #----------------------------------------------------------------
            # Inputs & Movement:
            
            if pieceChosen == True: # If a piece has been selected
                if ev.type == pygame.KEYDOWN:
                    if blackPiece[selectedIndex][1] > 0: # If the piece is not at the top of the screen
                        if leftMove(-1, blackPiece, blackStatus, redPiece, redStatus, 'q') == True: # If the leftMove function allows a black piece to move, change programState
                            programState = 'Player 2 Turn'
                        if rightMove(-1, blackPiece, blackStatus, redPiece, redStatus, 'e') == True: # If the rightMove function allows a black piece to move, change programState
                            programState = 'Player 2 Turn'
                            
                        blackColour[selectedIndex] = black # Reset the colour of the piece and the pieceChosen variable
                        pieceChosen = False
                            
                    if blackPiece[selectedIndex][1] < 7: # If the piece is not at the bottom of the screen
                        if blackKing[selectedIndex] == 'King': # If the selected index has the characteristic 'King' in its king variable
                            if leftMove(1, blackPiece, blackStatus, redPiece, redStatus, 'a') == True: # If the leftMove function allows a black piece to move (in the opposite direction than a regular movement), change programState
                                programState = 'Player 2 Turn'
                            if rightMove(1, blackPiece, blackStatus, redPiece, redStatus, 'd') == True: # If the rightMove function allows a black piece to move (in the opposite direction than a regular movement), change programState
                                programState = 'Player 2 Turn'
                        
                            blackColour[selectedIndex] = black # Reset the colour of the piece and the pieceChosen variable
                            pieceChosen = False
                        
                        
            #----------------------------------------------------------------
            
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            pygame.draw.rect(mainSurface, white, (72, 72, tileWidth*8, tileHeight*8))# Draw the white "tiles" (Background square)
            mainSurface.blit(renderedTurnShow, turnTextPos)
            
            for i in range(0, len(tiles), 1): # Draw grey tiles
                tiles[i].drawTile(mainSurface)
            
            drawPieces() # Run the draw pieces function
        
        
        elif programState == 'Player 2 Turn':
            # Update your game objects and data structures here...
            
            kingCheck() # Check if any pieces are eligible to be a king piece
            
            if deadCheck() == 'Player 1 is dead': # Check if player 1's pieces are dead, end game if so
                programState = 'End Screen'
                gameWinner = '2'
            elif deadCheck() == 'Player 2 is dead': # Check if player 2's pieces are dead, end game if so
                programState = 'End Screen'
                gameWinner = '1'
            
            renderedTurnShow = buttonFont.render("Player 2's Turn", True, red)
            
            if ev.type == pygame.KEYDOWN: # If a key was pressed
                if ev.scancode == 41: # If the key was the esc key, record the programState and go to pause menu
                    previousState = programState
                    programState = 'Pause Menu'
            
            if ev.type == pygame.MOUSEBUTTONDOWN: # Is there a mouse event
                if pieceChosen == False: # If no piece has been selected
                    for i in range(0, len(redPiece), 1): # Check all red piece indexes
                        if distFromPoints(board[redPiece[i][1]][redPiece[i][0]], mousePos) < pieceRadius: # If there is a collision between the mouse and a red piece
                            if redStatus[i] == 'Alive': # Check if the piece is alive
                                pieceChosen = True
                                selectedIndex = i # Temp variable to hold the index of the piece in the piece list
                                redColour[selectedIndex] = yellow
            
            #----------------------------------------------------------------
            # Inputs & Movement:
            
            if pieceChosen == True: # If a piece has been selected
                if ev.type == pygame.KEYDOWN:
                    if redPiece[selectedIndex][1] < 7: #If the piece is not at the bottom of the screen
                        if leftMove(1, redPiece, redStatus, blackPiece, blackStatus, 'a') == True: # If the leftMove function allows a red piece to move, change programState
                            programState = 'Player 1 Turn'
                        if rightMove(1, redPiece, redStatus, blackPiece, blackStatus, 'd') == True: # If the right Move function allows a red piece to move, change programState
                            programState = 'Player 1 Turn'
                            
                        redColour[selectedIndex] = red # Reset the colour of the piece and the pieceChosen variable
                        pieceChosen = False
                    
                    if redPiece[selectedIndex][1] > 0: # If the piece is not at the top of the screen
                        if redKing[selectedIndex] == 'King': # If the selected index has the characteristic 'King' in its king variable
                            if leftMove(-1, redPiece, redStatus, blackPiece, blackStatus, 'q') == True: # If the leftMove function allows a red piece to move (in the opposite direction than a regular movement), change programState
                                programState = 'Player 1 Turn'
                            if rightMove(-1, redPiece, redStatus, blackPiece, blackStatus, 'e') == True: # If the rightMove function allows a red piece to move (in the opposite direction than a regular movement), change programState
                                programState = 'Player 1 Turn'
                        
                            redColour[selectedIndex] = red # Reset the colour of the piece and the pieceChosen variable
                            pieceChosen = False
                
            
            #----------------------------------------------------------------
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            pygame.draw.rect(mainSurface, white, (72, 72, tileWidth*8, tileHeight*8))# Draw the white "tiles" (Background square)
            mainSurface.blit(renderedTurnShow, turnTextPos)
            
            for i in range(0, len(tiles), 1): # Draw grey tiles
                tiles[i].drawTile(mainSurface)
            
            drawPieces() # Run the draw pieces function
            
            
        elif programState == 'End Screen':
            # Update your game objects and data structures here...
                
            # Reset variables so last game will be overwritten (when a player wins, the save is reset to a new game)
            redPiece = [ [0, 0,], [2, 0], [4, 0], [6, 0], [1, 1], [3, 1], [5, 1], [7, 1] ]
            redStatus = [ 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive']
            redKing = ['Notking', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing']
            redColour = [red, red, red, red, red, red, red, red]
            blackPiece = [ [0, 6], [2, 6], [4, 6], [6, 6], [1, 7], [3, 7], [5, 7], [7, 7] ]
            blackStatus = [ 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive']
            blackKing = ['Notking', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing', 'NotKing']
            blackColour = [black, black, black, black, black, black, black, black]
            previousState = 'Player 1 Turn'
            
            writeInfo() # Write the game info using the writeInfo function
            
            # Text rendering
            renderedWin = titleFont.render(f'Player {gameWinner} Wins!', True, white)
            renderedEndBack = buttonFont.render('Back to Menu', True, black)
            
            if endBackButton.buttonCollidePoint(mousePos) == True: # Check if the back to menu button has been pressed
                programState = 'Start Menu'
                
                
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            # Button Drawing
            endBackButton.draw(mainSurface)
            
            # Text drawing
            mainSurface.blit(renderedWin, (165, 100))
            mainSurface.blit(renderedEndBack, (285, 455))
            
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower

    pygame.quit()     # Once we leave the loop, close the window.

main()