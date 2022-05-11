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
import random
import math
    
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
    piecePos = [144-tileWidth/2, 108]
    pieceRadius = 30
    pieceXPositions = (180, 324, 468, 612, 108, 252, 396, 540) #List of x values to help determine which diagonal part of the board the piece is on
    pieceChosen = False
    
    #Continue Button Variables
    contButtonRect = [160, 420, 400, 50]
    
    #Fonts and Text
    titleFont = pygame.font.SysFont("Times New Roman", 65)
    buttonFont = pygame.font.SysFont("Times New Roman", 26)
    playerTurn = '1'
    
    # Board
    board = []
    boardX = []
    boardY = []
    
    for count in range(0, 8, 1):
        boardX.append( tilePos[0]*(count+1) + tileWidth/2)
    
    for count in range(0, 8, 1):
        boardY.append( tilePos[1]*(count+1) + tileHeight/2)
    
    print(boardX)
    print(boardY)
    
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
            
             
    class piece():
        def __init__(self, inputColour, inputPos, inputRadius):
            self.pos = inputPos
            self.colour = inputColour
            self.radius = inputRadius
            
        def drawPiece(self, inputSurface):
            '''
            Basic function that draws a singular piece on the surface given
            
            Parameters
            ----------
            inputSurface : (int, int, int)
                the surface at which the piece is drawn
                
            Returns
            -------
            None
            '''
            pygame.draw.circle(inputSurface, self.colour, [ self.pos[0], self.pos[1] ], self.radius)
        
        def distFromPoints(self, point):# Function from python notes, circle-button collision detection. Edited to better reflect the pieces
            '''
            This function calculationes the distance between two points given by a set of tuples (x1,y1) and (x2,y2)
            
            Parameters
            ----------
            point : (float, float)
                The point to compare
                
            Returns
            -------
            float
                The distance between the two points
            '''
            distance = math.sqrt( ((point[0]-self.pos[0])**2)+((point[1]-self.pos[1])**2) )
            
            return distance    
        
            
        def pieceMovement(self, direction, pieceColour):
            '''
            Function that moves pieces according to its inputs
            
            Uses the given str inputs in order to correctly move pieces. Pieces
            move differently due to the fact that red has to move down as opposed
            to black needing to move up on the screen.
            
            Parameters
            ----------
            direction : str
                Direction string that the piece is being told to move in
            pieceColour : str
                String on which team/"colour" the piece is
            
            Returns
            -------
            None
            '''
            if pieceColour == 'black':
                if direction == 'right':
                    self.pos[0] += tileWidth
                    self.pos[1] -= tileHeight
                     
                elif direction == 'left':
                     self.pos[0] -= tileWidth
                     self.pos[1] -= tileHeight
                     
            elif pieceColour == 'red':
                if direction == 'right':
                    self.pos[0] += tileWidth
                    self.pos[1] += tileHeight
                elif direction == 'left':
                    self.pos[0] -= tileWidth
                    self.pos[1] -= tileHeight
        
    #------Object Definitions------
    
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
            
    #--Pieces--
    
    pieces = [] # List of pieces
    
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
                for i in range(0, len(tiles), 1):
                    if tiles[i].tileCollidePoint(mousePos):
                        print(i)
            


            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            pygame.draw.rect(mainSurface, white, (72, 72, tileWidth*8, tileHeight*8))# Draw the white "tiles" (Background square)
            
            for i in range(0, len(tiles), 1): # Draw grey tiles
                tiles[i].drawTile(mainSurface)
                
            for i in range(0, len(pieces), 1): # Draw pieces
                pieces[i].drawPiece(mainSurface)
        
        
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
            
            for i in range(0, len(pieces), 1): # Draw pieces
                pieces[i].drawPiece(mainSurface)
            
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower

    pygame.quit()     # Once we leave the loop, close the window.

main()