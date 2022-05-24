#-----------------------------------------------------------------------------
# Name:        Assignment Template (assignment.py)
# Purpose:     A description of your program goes here.
#
# Author:      Gavin B.
# Created:     04-May-2022
# Updated:     16-May-2022
#-----------------------------------------------------------------------------
#I think this project deserves a level XXXXXX because ...
#
#Features Added:
#   ...
#   ...
#   ...
#-----------------------------------------------------------------------------

import pygame
import math

def distFromPoints(point1, point2):
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

def pauseCheck(scanCode, currentState):
    '''
    '''
    if scanCode == 41:
        return 'Pause Menu'
    else: return currentState

def main():
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 720   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower
    
    frameRate = 60
    frameCount = 0
    
    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
    
    #--Variables--
    
    programState = 'Start Menu'
    previousState = ''
    playerTurn = '1'
    
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
    
    #Continue Button Variables
    contButtonRect = [160, 420, 400, 50]
    
    #Fonts and Text
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
    
    #Piece Variables
    
    # Base Red Piece values (for reference, variables will get reset in file reading)
    redPiece = [ [0, 0,], [2, 0], [4, 0], [6, 0], [1, 1], [3, 1], [5, 1], [7, 1] ] # Red piece coordinates
    redStatus = [ 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive'] # Red piece alive/dead list
    redColour = [red, red, red, red, red, red, red, red] #Colours of the red pieces (For piece highlighting)
    
    # Base Black Piece values (for reference, variables will get reset in file reading)
    blackPiece = [ [0, 6], [2, 6], [4, 6], [6, 6], [1, 7], [3, 7], [5, 7], [7, 7] ] # Black piece coordinates
    blackStatus = [ 'dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive'] # Black piece alive/dead list
    blackColour = [black, black, black, black, black, black, black, black] #Colours of the black pieces (for piece highlighting)
    
    pieceRadius = 30 # Radius of the pieces
    pieceChosen = False # Statement on if a piece has been chosen or not
    canMove = True # Statement on if a piece has been allowed to move upon an input
    farSideBlocked = False # Statement regarding if a piece is in the way of jumping
    enemyPieceInWay = False
    
    
    #-----Reading Files-----
    # Reset the variables to be read into
    redPiece = []
    redStatus = []
    blackPiece = []
    blackStatus = []
    
    
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
    while True: # Forever while loop until there is nothing left to read in file (see the if len(theLine) statement)
        theLine = redStatFile.readline()
        theLine = theLine.strip('\n')
        if len(theLine) == 0: #If there is nothing on the line, break
            break
        
        redStatus.append(theLine) # Add the line to the redStatus
    redStatFile.close()
    
    # Read the black status
    blackStatFile = open('last_game_info/blackPieceStatus.txt', 'r')
    while True: # Forever while loop until there is nothing left to read in file (see the if len(theLine) statement)
        theLine = blackStatFile.readline()
        theLine = theLine.strip('\n')
        if len(theLine) == 0: #If there is nothing on the line, break
            break
        
        blackStatus.append(theLine) # Add the line to the blackStatus
    blackStatFile.close()
    
    
    #-Other File Reading-
    
    # Read the previous program state
    prevStateFile = open('last_game_info/previousGameState.txt', 'r')
    previousState = prevStateFile.readline()
    prevStateFile.close()
    
    
    
    #----Object Classes----
    
    class button(): #Class object for tiles and buttons
        def __init__(self, inputColour, inputRect):
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
            class's variables, checks if there is a mouse input & returns True if so
            (pressing button), else return False (not pressing button)


            Parameters
            ----------
            inPnt : int
                positional list of X & Y values used to be checked in if statement
              
            Returns
            -------
            boolean
                The statement regarding if the button was clicked or not
            '''
            if inPnt[0] > self.rect[0] and inPnt[0] < self.rect[0]+self.rect[2] and inPnt[1] < self.rect[1]+self.rect[3] and inPnt[1] > self.rect[1]:#Is the inpt colliding with button?
                if ev.type == pygame.MOUSEBUTTONDOWN: #Is there a mouse event?
                    return True
            else: return False
            
    
    class tile(): #Class object for tiles and buttons
        def __init__(self, inputColour, inputRect):
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
    
    playerOneContinue = button(green, contButtonRect)
    playerTwoContinue = button(green, contButtonRect)
    
    #--Tiles--
    
    tiles = [] # List of tiles/tile information for the program to draw from

    for count in range(0, 8, 1):#For loop that repeats 8 times, the number of rows
        for count in range(0, 4, 1): #For loop that repeats 8 times, the number of columns
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
        #print(f'Program Ticks: {pygame.time.get_ticks()} - programState: {programState}')
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
        
        mousePos = pygame.mouse.get_pos()#Mouse position for buttons
        
        frameCount+=1
        if frameCount >= 60:
            frameCount -= 60
        
        if programState == 'Start Menu':
            # Update your game objects and data structures here...
            
            renderedTitle = titleFont.render('Title', 12, white)
            renderedContinueGame = buttonFont.render('Continue Previous Game', 12, black)
            renderedNew = buttonFont.render('New Game', 12, black)
            renderedHelp = buttonFont.render('Help & Instructions', 12, black)
            renderedExit = buttonFont.render('Exit', 12, black)
            
            if continueGameButton.buttonCollidePoint(mousePos) == True:
                programState = previousState
                
            elif newGameButton.buttonCollidePoint(mousePos) == True:
                redPiece = [ [0, 0,], [2, 0], [4, 0], [6, 0], [1, 1], [3, 1], [5, 1], [7, 1] ]
                redStatus = [ 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive']
                redColour = [red, red, red, red, red, red, red, red]
                blackPiece = [ [0, 6], [2, 6], [4, 6], [6, 6], [1, 7], [3, 7], [5, 7], [7, 7] ]
                blackStatus = [ 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive']
                blackColour = [black, black, black, black, black, black, black, black]
                programState = 'Player 1 Continue'
                
            elif helpButton.buttonCollidePoint(mousePos) == True:
                programState = 'Help Menu'
                
            elif exitButton.buttonCollidePoint(mousePos) == True:
                
                # Write last known red coordinates
                redCoordFile = open('last_game_info/redPieceCoordinates.txt', 'w')
                for i in range(0, 8, 1):
                    redCoordFile.write(f'{redPiece[i][0]}\n{redPiece[i][1]}\n')
                redCoordFile.close()
                
                # Write last known black coordinates
                blackCoordFile = open('last_game_info/blackPieceCoordinates.txt', 'w')
                for i in range(0, 8, 1):
                    blackCoordFile.write(f'{blackPiece[i][0]}\n{blackPiece[i][1]}\n')
                blackCoordFile.close()
                
                # Write last known red status list
                redStatFile = open('last_game_info/redPieceStatus.txt', 'w')
                
                #redStatFile.write(f'dead\nAlive\nAlive\nAlive\nAlive\nAlive\nAlive\nAlive\n')
                for i in range(0, 8, 1):
                    redStatFile.write(f'{redStatus[i]}\n')
                redStatFile.close()
                
                # Write last known black status list
                blackStatFile = open('last_game_info/blackPieceStatus.txt', 'w')
                for i in range(0, 8, 1):
                    blackStatFile.write(f'{blackStatus[i]}\n')
                blackStatFile.close()
                
                break
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            newGameButton.draw(mainSurface)
            continueGameButton.draw(mainSurface)
            helpButton.draw(mainSurface)
            exitButton.draw(mainSurface)
            
            mainSurface.blit(renderedTitle, (300, 100))
            mainSurface.blit(renderedContinueGame, (235, 360))
            mainSurface.blit(renderedNew, (300, 455))
            mainSurface.blit(renderedHelp, (260, 535))
            mainSurface.blit(renderedExit, (340, 600))
            
            
        elif programState == 'Help Menu':
            # Update your game objects and data structures here...
            
            if helpExit.buttonCollidePoint(mousePos) == True:
                programState = 'Start Menu'
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            helpExit.draw(mainSurface)
        
        
        elif programState == 'Pause Menu':
            # Update your game objects and data structures here...
            
            if pauseContinue.buttonCollidePoint(mousePos) == True:
                programState = previousState
            elif pauseMainMenu.buttonCollidePoint(mousePos) == True:
                programState = 'Start Menu'
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            pauseContinue.draw(mainSurface)
            pauseMainMenu.draw(mainSurface)
            
            
        elif programState == 'Player 1 Continue':
            # Update your game objects and data structures here...
            
            if ev.type == pygame.KEYUP:
                previousState = programState
                programState = pauseCheck(ev.scancode, programState)
            
            playerTurn = '1'
            renderedTurnContinue = buttonFont.render('Take Turn!', 12, black)
            renderedTurnDeclare = titleFont.render(f"Player {playerTurn}'s Turn", 12, white)
            
            if playerOneContinue.buttonCollidePoint(mousePos):
                pieceChosen = False
                programState = 'Player 1 Turn'
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            pygame.draw.rect(mainSurface, white, (72, 72, tileWidth*8, tileHeight*8))# Draw the white "tiles" (Background square)
            
            for i in range(0, len(tiles), 1): # Draw grey tiles
                tiles[i].drawTile(mainSurface)
            
            playerOneContinue.draw(mainSurface)
            pygame.draw.rect(mainSurface, black, (140, 120, 440, 80))
            mainSurface.blit(renderedTurnDeclare, (160, 120))
            mainSurface.blit(renderedTurnContinue, (300, 430))
            
            
        elif programState == 'Player 1 Turn':
            # Update your game objects and data structures here...
            
            if ev.type == pygame.KEYUP:
                previousState = programState
                programState = pauseCheck(ev.scancode, programState)
            
            if ev.type == pygame.MOUSEBUTTONDOWN: # Is there a mouse event
                if pieceChosen == False: # If no piece has been selected
                    for i in range(0, len(blackPiece), 1): # Check all black piece indexes
                        if distFromPoints(board[blackPiece[i][1]][blackPiece[i][0]], mousePos) < pieceRadius: # If there is a collision between the mouse and a black piece
                            if blackStatus[i] == 'Alive': # Check if the piece is alive
                                pieceChosen = True
                                a = i # Temp variable to hold the index of the piece in the piece list
                                blackColour[a] = yellow
            
            #----------------------------------------------------------------
            # Inputs & Movement:
            
            if pieceChosen == True: # If a piece has been selected
                if ev.type == pygame.KEYDOWN:
                    
                    if blackPiece[a][1]-1 >= 0: #If the piece above is not overtop the screen
                        
                        #---------------Left Side---------------
                        
                        if ev.unicode == 'a' or ev.scancode == 80: # Check for input
                            if blackPiece[a][0]-1 >= 0: # If the tile is not on the left edge
                                canMove = True
                                farSideBlocked = False
                                enemyPieceInWay = False
                                
                                for i in range(0, 8, 1): # Do this 8 times, number of piece indexes for red and black pieces
                                    if blackStatus[i] == 'Alive':
                                        if blackPiece[i][0] == (blackPiece[a][0]-1) and blackPiece[i][1] == (blackPiece[a][1]-1): #Check for a black piece to the top left
                                            canMove = False
                                            pieceChosen = False
                                        
                                    if redStatus[i] == 'Alive':
                                        if redPiece[i][0] == (blackPiece[a][0]-1) and redPiece[i][1] == (blackPiece[a][1]-1):#Check for a red piece to the top left
                                            enemyPieceInWay = True
                                            j = i #Temp record the index of the red piece (in the case it needs to be killed)
                                            
                                            for count in range(0, 8, 1): # Do this 8 times, number of pieces on each side
                                                if redPiece[count][0] == (blackPiece[a][0]-2) and redPiece[count][1] == (blackPiece[a][1]-2) and redStatus[count] == 'Alive':
                                                    farSideBlocked = True
                                                if blackPiece[count][0] == (blackPiece[a][0]-2) and blackPiece[count][1] == (blackPiece[a][1]-2) and blackStatus[count] == 'Alive':
                                                    farSideBlocked = True
                                            
                                            canMove = False
                                            pieceChosen = False
                                
                                if farSideBlocked == False and enemyPieceInWay == True:
                                    if (blackPiece[a][0]-2) >= 0 and (blackPiece[a][1]-2) >= 0: # If the tile two to the left, two up is on the board, jump and reset
                                        blackPiece[a][1] -= 2
                                        blackPiece[a][0] -= 2
                                        redStatus[j] = 'Dead' # Kill the red piece
                                        pieceChosen = False
                                        blackColour[a] = black
                                        programState = 'Player 2 Continue'
                                        canMove = False
                                    else: # The piece cannot jump, reset
                                        pieceChosen = False
                                        blackColour[a] = black
                                        canMove = False
                                        
                                if canMove == True:
                                    blackPiece[a][1] -= 1
                                    blackPiece[a][0] -= 1
                                    pieceChosen = False
                                    blackColour[a] = black
                                    programState = 'Player 2 Continue'
                                        
                                else:# Reset the piece chosen
                                    pieceChosen = False
                                    blackColour[a] = black
                                    
                            else:# Reset the piece chosen
                                pieceChosen = False
                                blackColour[a] = black
                                            
                        else: # Reset the piece chosen
                            pieceChosen = False
                            blackColour[a] = black
                        
                        #---------------Right Side--------------
                        
                        if ev.unicode == 'd' or ev.scancode == 79: # Check for input
                            if blackPiece[a][0]+1 <= 7: # If the tile is not on the right edge
                                canMove = True
                                farSideBlocked = False
                                enemyPieceInWay = False
                                
                                for i in range(0, 8, 1): # Do this 8 times, number of piece indexes for red and black pieces
                                    if blackStatus[i] == 'Alive':
                                        if blackPiece[i][0] == (blackPiece[a][0]+1) and blackPiece[i][1] == (blackPiece[a][1]-1): #Check for a black piece to the top right  
                                            canMove = False
                                            pieceChosen = False
                                    
                                    if redStatus[i] == 'Alive':
                                        if redPiece[i][0] == (blackPiece[a][0]+1) and redPiece[i][1] == (blackPiece[a][1]-1):#Check for a red piece to the top right
                                            enemyPieceInWay = True
                                            j = i #Temp record the index of the red piece (in the case it needs to be killed)
                                            
                                            for count in range(0, 8, 1): # Do this 8 times, number of pieces on each side
                                                if redPiece[count][0] == (blackPiece[a][0]+2) and redPiece[count][1] == (blackPiece[a][1]-2) and redStatus[count] == 'Alive':
                                                    farSideBlocked = True
                                                if blackPiece[count][0] == (blackPiece[a][0]+2) and blackPiece[count][1] == (blackPiece[a][1]-2) and blackStatus[count] == 'Alive':
                                                    farSideBlocked = True
                                                
                                            canMove = False
                                            pieceChosen = False
                                        
                                if farSideBlocked == False and enemyPieceInWay == True:
                                    if (blackPiece[a][0]+2) <= 7 and (blackPiece[a][1]-2) >= 0: # If the tile two to the right, two up is on the board, jump and reset
                                        blackPiece[a][1] -= 2
                                        blackPiece[a][0] += 2
                                        redStatus[j] = 'Dead' # Kill the red piece
                                        blackColour[a] = black
                                        programState = 'Player 2 Continue'
                                        canMove = False
                                    else: # The piece cannot jump, reset
                                        pieceChosen = False
                                        blackColour[a] = black
                                        canMove = False
                                        
                                if canMove == True:
                                    blackPiece[a][1] -= 1
                                    blackPiece[a][0] += 1
                                    pieceChosen = False
                                    blackColour[a] = black
                                    programState = 'Player 2 Continue'
                                else: # Reset the piece chosen
                                    pieceChosen = False
                                    blackColour[a] = black
                            else:# Reset the piece chosen
                                pieceChosen = False
                                blackColour[a] = black
                        else: # Reset the piece chosen
                            pieceChosen = False
                            blackColour[a] = black
                            
                    else: # Reset the piece chosen
                        pieceChosen = False
                        blackColour[a] = black
                
            #----------------------------------------------------------------
            
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            pygame.draw.rect(mainSurface, white, (72, 72, tileWidth*8, tileHeight*8))# Draw the white "tiles" (Background square)
            
            for i in range(0, len(tiles), 1): # Draw grey tiles
                tiles[i].drawTile(mainSurface)
            for i in range(0, len(redPiece), 1): # Draw red pieces
                if redStatus[i] == 'Alive': # Check if the piece is alive
                    pygame.draw.circle(mainSurface, redColour[i], board[redPiece[i][1]][redPiece[i][0]], pieceRadius)
            for i in range(0, len(blackPiece), 1): # Draw black pieces
                if blackStatus[i] == 'Alive': # Check if the piece is alive
                    pygame.draw.circle(mainSurface, blackColour[i], board[blackPiece[i][1]][blackPiece[i][0]], pieceRadius)
        
        
        elif programState == 'Player 2 Continue':
            # Update your game objects and data structures here...
            if ev.type == pygame.KEYUP:
                previousState = programState
                programState = pauseCheck(ev.scancode, programState)
            
            playerTurn = '2'
            renderedTurnContinue = buttonFont.render('Take Turn!', 12, black)
            renderedTurnDeclare = titleFont.render(f"Player {playerTurn}'s Turn", 12, red)
            
            if playerTwoContinue.buttonCollidePoint(mousePos):
                pieceChosen = False
                programState = 'Player 2 Turn'
            
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            pygame.draw.rect(mainSurface, white, (72, 72, tileWidth*8, tileHeight*8))# Draw the white "tiles" (Background square)
            
            for i in range(0, len(tiles), 1): # Draw grey tiles
                tiles[i].drawTile(mainSurface)
            
            playerTwoContinue.draw(mainSurface)
            pygame.draw.rect(mainSurface, black, (140, 120, 440, 80))
            mainSurface.blit(renderedTurnDeclare, (160, 120))
            mainSurface.blit(renderedTurnContinue, (300, 430))
        
        elif programState == 'Player 2 Turn':
            # Update your game objects and data structures here...
            if ev.type == pygame.KEYUP:
                previousState = programState
                programState = pauseCheck(ev.scancode, programState)
            
            if ev.type == pygame.MOUSEBUTTONDOWN: # Is there a mouse event
                if pieceChosen == False: # If no piece has been selected
                    for i in range(0, len(redPiece), 1): # Check all red piece indexes
                        if distFromPoints(board[redPiece[i][1]][redPiece[i][0]], mousePos) < pieceRadius: # If there is a collision between the mouse and a red piece
                            if redStatus[i] == 'Alive': # Check if the piece is alive
                                pieceChosen = True
                                a = i # Temp variable to hold the index of the piece in the piece list
                                redColour[a] = yellow
            
            #----------------------------------------------------------------
            # Inputs & Movement:
            
            if pieceChosen == True: # If a piece has been selected
                if ev.type == pygame.KEYDOWN:
                    
                    if redPiece[a][1] < 7: #If the piece is not at the bottom of the screen
                        
                        #---------------Left Side---------------
                        
                        if ev.unicode == 'a' or ev.scancode == 80: # Check for input
                            if redPiece[a][0]-1 >= 0: # If the left tile exists/is on the board
                                canMove = True
                                farSideBlocked = False
                                enemyPieceInWay = False
                                
                                for i in range(0, 8, 1): # Do this 8 times, number of piece indexes for red and black pieces
                                    if redStatus[i] == 'Alive':
                                        if redPiece[i][0] == (redPiece[a][0]-1) and redPiece[i][1] == (redPiece[a][1]+1): #Check for a red piece to the bottom left
                                            canMove = False
                                            pieceChosen = False
                                    if blackStatus[i] == 'Alive':
                                        if blackPiece[i][0] == (redPiece[a][0]-1) and blackPiece[i][1] == (redPiece[a][1]+1):#Check for a black piece to the bottom left
                                            enemyPieceInWay = True
                                            j = i #Temp record the index of the red piece (in the case it needs to be killed)
                                        
                                            for count in range(0, 8, 1): # Do this 8 times, number of pieces on each side
                                                if blackPiece[count][0] == (redPiece[a][0]-2) and blackPiece[count][1] == (redPiece[a][1]+2) and blackStatus[count] == 'Alive': # Check for a red piece in the way of a left jump
                                                    farSideBlocked = True
                                                if redPiece[count][0] == (redPiece[a][0]-2) and redPiece[count][1] == (blackPiece[a][1]+2) and redStatus[count] == 'Alive': # Check for a red piece in the way of a left jump
                                                    farSideBlocked = True
                                            
                                            canMove = False
                                            pieceChosen = False
                                            
                                if farSideBlocked == False and enemyPieceInWay == True:
                                    if (redPiece[a][0]-2) >= 0 and (redPiece[a][1]+2) <= 7: # If the tile two to the left, two up is on the board, jump and reset
                                        redPiece[a][1] += 2
                                        redPiece[a][0] -= 2
                                        blackStatus[j] = 'Dead' # Kill the black piece
                                        pieceChosen = False
                                        redColour[a] = red
                                        programState = 'Player 1 Continue'
                                        canMove = False
                                      
                                if canMove == True:
                                    redPiece[a][1] += 1
                                    redPiece[a][0] -= 1
                                    pieceChosen = False
                                    redColour[a] = red
                                    programState = 'Player 1 Continue'
                                else: # Reset the piece chosen
                                    pieceChosen = False
                                    redColour[a] = red
                            else: # Reset the piece chosen
                                pieceChosen = False
                                redColour[a] = red
                            
                        else: # Reset the piece chosen
                            pieceChosen = False
                            redColour[a] = red
                        
                        #---------------Right Side--------------
                        
                        if ev.unicode == 'd' or ev.scancode == 79: # Check for input
                            if redPiece[a][0]+1 <= 7: # If the right tile exists/is on the board
                                canMove = True
                                farSideBlocked = False
                                enemyPieceInWay = False
                                
                                for i in range(0, 8, 1): # Do this 8 times, number of piece indexes for red and black pieces
                                    if redStatus[i] == 'Alive':
                                        if redPiece[i][0] == (redPiece[a][0]+1) and redPiece[i][1] == (redPiece[a][1]+1): #Check for a piece to the bottom right
                                            canMove = False
                                            pieceChosen = False
                                    if blackStatus[i] == 'Alive':
                                        if blackPiece[i][0] == (redPiece[a][0]+1) and blackPiece[i][1] == (redPiece[a][1]+1):#Check for a red piece to the bottom right
                                            enemyPieceInWay = True
                                            j = i #Temp record the index of the red piece (in the case it needs to be killed)
                                        
                                            for count in range(0, 8, 1): # Do this 8 times, number of pieces on each side
                                                if blackPiece[count][0] == (redPiece[a][0]+2) and blackPiece[count][1] == (redPiece[a][1]+2) and blackStatus[count] == 'Alive':
                                                    farSideBlocked = True
                                                if redPiece[count][0] == (redPiece[a][0]+2) and redPiece[count][1] == (redPiece[a][1]+2) and redStatus[count] == 'Alive':
                                                    farSideBlocked = True
                                            
                                            canMove = False
                                            pieceChosen = False
                                        
                                if farSideBlocked != True and enemyPieceInWay == True:
                                    if (redPiece[a][0]+2) <= 7 and (redPiece[a][1]-2) <= 7: # If the tile two to the right, two up is on the board, jump and reset
                                        redPiece[a][1] += 2
                                        redPiece[a][0] += 2
                                        blackStatus[j] = 'Dead' # Kill the black piece
                                        pieceChosen = False
                                        redColour[a] = red
                                        programState = 'Player 1 Continue'
                                        canMove = False
                                        
                                if canMove == True:
                                    redPiece[a][1] += 1
                                    redPiece[a][0] += 1
                                    pieceChosen = False
                                    redColour[a] = red
                                    programState = 'Player 1 Continue'
                                else: # Reset the piece chosen
                                    pieceChosen = False
                                    redColour[a] = red
                                    
                            else: # Reset the piece chosen
                                pieceChosen = False
                                redColour[a] = red
                                
                        else: # Reset the piece chosen
                            pieceChosen = False
                            redColour[a] = red
                            
                    else: # Reset the piece chosen
                        pieceChosen = False
                        redColour[a] = red
                
                
            
            #----------------------------------------------------------------
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            pygame.draw.rect(mainSurface, white, (72, 72, tileWidth*8, tileHeight*8))# Draw the white "tiles" (Background square)
            
            for i in range(0, len(tiles), 1): # Draw grey tiles
                tiles[i].drawTile(mainSurface)
            for i in range(0, len(redPiece), 1): # Draw red pieces
                if redStatus[i] == 'Alive': # Check if the piece is alive
                    pygame.draw.circle(mainSurface, redColour[i], board[redPiece[i][1]][redPiece[i][0]], pieceRadius)
            for i in range(0, len(blackPiece), 1): # Draw black pieces
                if blackStatus[i] == 'Alive': # Check if the piece is alive
                    pygame.draw.circle(mainSurface, blackColour[i], board[blackPiece[i][1]][blackPiece[i][0]], pieceRadius)
            
            
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower

    pygame.quit()     # Once we leave the loop, close the window.

main()