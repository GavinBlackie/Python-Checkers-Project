#-----------------------------------------------------------------------------
# Name:        Assignment Template (assignment.py)
# Purpose:     A description of your program goes here.
#
# Author:      Gavin B.
# Created:     04-May-2022
# Updated:     08-May-2022
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

def main():
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 720   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
    #--Variables--
    programState = 'Player 1 Continue'
    
    #Colours:
    white = (255, 255, 255)
    grey = (140, 140, 140)
    black = (0, 0, 0)
    red = (255, 0, 0)
    yellow = (229, 255, 0)
    green = (0, 255, 0)
    
    #Tile Variables
    tilePos = [72, 72]
    tileWidth = 72
    tileHeight = 72
    tileShift = False
    
    #Piece Variables
    piecePos = [108, 108]
    pieceRadius = 30
    pieceChosen = False
    
    #Continue Button Variables
    contButtonRect = [160, 420, 400, 50]
    
    #Fonts and Text
    titleFont = pygame.font.SysFont("Times New Roman", 65)
    buttonFont = pygame.font.SysFont("Times New Roman", 26)
    playerTurn = '1'
    
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
    redPiece = [ [0, 0], [2, 0], [4, 0], [6, 0], [1, 1], [3, 1], [5, 1], [7, 1] ] # Red piece coordinates
    blackPiece = [ [0, 6], [2, 6], [4, 6], [6, 6], [1, 7], [3, 7], [5, 7], [7, 7] ] # Black piece coordinates
    pieceRadius = 30 # Radius of the pieces
    pieceChosen = False # Statement on if a piece has been chosen or not
    
    
    #--Object Classes--
    
    class button(): #Class object for tiles and buttons
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
            
        #Collide function, checks wheter or not the input point is within the button's boundaries (Function from my mini-game assignment)
        def tileCollidePoint(self, inPnt):
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
            
        def clicked(self, inputColour):
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
        
        #Collide function, checks wheter or not the input point is within the button's boundaries (Function from my mini-game assignment)
        def tileCollidePoint(self, inPnt):
            '''
            Function that returns True or False depending on whether or not the if statements are fullfilled.
              
            Check if colour of tile is correct (grey or green). Takes the inPnt parameter, if it is within the boundaries of the button
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
            if self.colour == grey or self.colour == green:
                if inPnt[0] > self.rect[0] and inPnt[0] < self.rect[0]+self.rect[2] and inPnt[1] < self.rect[1]+self.rect[3] and inPnt[1] > self.rect[1]:#Is the inpt colliding with button?
                    if ev.type == pygame.MOUSEBUTTONDOWN: #Is there a mouse event?
                        return True
            else: return False
            
        
    #------Object Definitions (Initializations)------
    
    #--Buttons--
    
    playerOneContinue = button(green, contButtonRect)
    playerTwoContinue = button(green, contButtonRect)
    
    
    #--Tiles--
    
    tiles = [] # List of tiles/tile information for the program to draw from

    for y in range(0, 8, 1):#For loop that repeats 8 times, the number of rows
        for x in range(0, 4, 1): #For loop that repeats 8 times, the number of columns
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
        renderedTurnContinue = buttonFont.render('Take Turn!', 12, black)
        
        if programState == 'Player 1 Continue':
            # Update your game objects and data structures here...
            playerTurn = '1'
            renderedTurnDeclare = titleFont.render(f"Player {playerTurn}'s Turn", 12, white)
            
            if playerOneContinue.tileCollidePoint(mousePos):
                programState = 'Player 1 Turn'
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            playerOneContinue.drawTile(mainSurface)
            mainSurface.blit(renderedTurnDeclare, (160, 120))
            mainSurface.blit(renderedTurnContinue, (300, 430))
            
        elif programState == 'Player 1 Turn':
            # Update your game objects and data structures here...

            if ev.type == pygame.MOUSEBUTTONDOWN: # Is there a mouse event
                if pieceChosen == False: # If no piece has been selected
                    for i in range(0, len(blackPiece), 1): # Check all black piece indexes
                        if distFromPoints(board[blackPiece[i][1]][blackPiece[i][0]], mousePos) < pieceRadius: # If there is a collision between the mouse and a black piece
                            pieceChosen = True
                            a = i
            if pieceChosen == True: # If a piece has been selected
                print(blackPiece[a])
                
                if ev.type == pygame.KEYDOWN:
                    if ev.unicode == 'a' or ev.scancode == 80:
                        blackPiece[a][1] -= 1
                        blackPiece[a][0] -= 1
                        pieceChosen = False
                    elif ev.unicode == 'd' or ev.scancode == 79:
                        blackPiece[a][1] -= 1
                        blackPiece[a][0] += 1
                        pieceChosen = False
                
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            pygame.draw.rect(mainSurface, white, (72, 72, tileWidth*8, tileHeight*8))# Draw the white "tiles" (Background square)
            
            for i in range(0, len(tiles), 1): # Draw grey tiles
                tiles[i].drawTile(mainSurface)
            for i in range(0, len(redPiece), 1): # Draw red pieces
                pygame.draw.circle(mainSurface, red, board[redPiece[i][1]][redPiece[i][0]], pieceRadius)
            for i in range(0, len(blackPiece), 1): # Draw black pieces
                pygame.draw.circle(mainSurface, black, board[blackPiece[i][1]][blackPiece[i][0]], pieceRadius)
        
        
        elif programState == 'Player 2 Continue':
            # Update your game objects and data structures here...
            playerTurn = '2'
            renderedTurnDeclare = titleFont.render(f"Player {playerTurn}'s Turn", 12, red)
            
            if playerTwoContinue.tileCollidePoint(mousePos):
                programState = 'Player 2 Turn'
            
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            playerTwoContinue.drawTile(mainSurface)
            mainSurface.blit(renderedTurnDeclare, (160, 120))
            mainSurface.blit(renderedTurnContinue, (300, 430))
        
        elif programState == 'Player 2 Turn':
            # Update your game objects and data structures here...
            
                    
            mousePos = pygame.mouse.get_pos()#Mouse position for buttons
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            pygame.draw.rect(mainSurface, white, (72, 72, tileWidth*8, tileHeight*8))# Draw the white "tiles" (Background square)
            
            for i in range(0, len(tiles), 1): # Draw tiles
                tiles[i].drawTile(mainSurface)
            
            
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower

    pygame.quit()     # Once we leave the loop, close the window.

main()