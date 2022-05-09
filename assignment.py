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
    isTileWhite = True
    
    #Piece Variables
    piecePos = [108+tileWidth, 108]
    pieceRadius = 30
    pieceXPositions = (180, 324, 468, 612, 108, 252, 396, 540) #List of x values to help determine which diagonal part of the board the piece is on
    
    #Continue Button Variables
    contButtonRect = [160, 420, 400, 50]
    
    #Fonts and Text
    titleFont = pygame.font.SysFont("Times New Roman", 65)
    buttonFont = pygame.font.SysFont("Times New Roman", 26)
    playerTurn = '1'
    
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
              
            Check if colour of tile is correct (grey). Takes the inPnt parameter, if it is within the boundaries of the button
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
            if self.colour == grey:
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
        
        def whichDiagonal(self, lifeStatus):
            '''
            Basic function that takes in a boolean to say if the piece is alive, if so
            it will check a list to see which diagonal part of the board the piece is on.
            
            Parameters
            ----------
            lifeStatus : boolean
                The statement on if the tile is alive
            
            Returns
            -------
            boolean
                Statement on which diagonal the piece is on
            
            '''
            if lifeStatus == True:
                for i in range(0, len(pieceXPositions)-4, 1):
                    if self.pos[0] == pieceXPositions[i]:
                        return True
                    
                for i in range(4, len(pieceXPositions), 1):
                    if self.pos[0] == pieceXPositions[i]:
                        return False
                    

    #------Object Definitions------
    
    #--Buttons--
    
    playerOneContinue = button(green, contButtonRect)
    playerTwoContinue = button(green, contButtonRect)
    
    
    #--Tiles--
    
    tiles = [] # List of tiles/tile information for the program to draw from
    
    # Load Tile Format into tiles list using for loops
    for y in range(0, 8, 1): #For loop that repeats 8 times, the number of rows
        
        for x in range(0, 8, 1): #For loop that repeats 8 times, the number of columns
            if isTileWhite == True: # Add a white tile if True
                tiles.append(tile( white, [tilePos[0], tilePos[1], tileWidth, tileHeight] ))
                tilePos[0] += tileWidth
            elif isTileWhite == False: # Add a grey tile if False
                tiles.append(tile( grey, [tilePos[0], tilePos[1], tileWidth, tileHeight] ))
                tilePos[0] += tileWidth
            isTileWhite = not isTileWhite # Alternate the colour along the x axis
            
        tilePos[1] += tileHeight #Add the y for the next line of tiles
        tilePos[0] -= tileWidth*8 # Decrease the x of the tiles by 8 times the width of one tile (the length of the board)
        isTileWhite = not isTileWhite # Alternate the colour along the y axis (create grid pattern instead of straight red & white lines)
    
    
    #--Pieces--
    
    pieces = []
    
    def loadPieces(pieceColour, piecePos): #Function to add pieces to piece list
        for y in range(0, 2, 1):
            for x in range(0, 4, 1):
                pieces.append(piece (pieceColour, [ piecePos[0], piecePos[1] ], pieceRadius) )
                piecePos[0] += tileWidth*2
            piecePos[1] += tileHeight
            piecePos[0] -= tileWidth*9
        return pieces
    
    loadPieces(red, piecePos)#Red pieces
    piecePos[1]+=tileWidth*4 #Reset the piecePos variables
    piecePos[0]+=tileWidth*2
    loadPieces(black, piecePos)#Black pieces

    
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
            
            if ev.type == pygame.KEYDOWN:
                for i in range(0, len(tiles), 1):
                    tiles[i].clicked(grey)
            
            for i in range(0, len(tiles), 1):
                if tiles[i].tileCollidePoint(mousePos):
                    tiles[i].clicked(green)
            
            if ev.type == pygame.MOUSEBUTTONDOWN: # Is there a mouse event
                for i in range(len(pieces)-8, len(pieces), 1): # Check all pieces with their indexes between 8 and 16 (black pieces)
                    if pieces[i].distFromPoints(mousePos) < pieceRadius: # Has a piece been clicked?
                        
                        #If/Elif statement to find out which diagonal the piece is on
                        if pieces[i].whichDiagonal(True) == True: #Is the piece on the "True" diagonal
                            print('true diag')
                            
                            tiles[2*i + 24].clicked(green) #Highlight tile on the left
                            
                            if (2*i + 26) < 47: #Highlight tile on the right, only if it does not go over the border
                                tiles[2*i + 26].clicked(green)
                                
                        elif pieces[i].whichDiagonal(True) == False: #Is the piece on the "False" diagonal
                            print('false diag')
                            
                            if (2*i + 23) > 47: #Highlight the tile on the left, only if it does not go over the border
                                tiles[2*i + 23].clicked(green)
                                
                            tiles[2*i + 25].clicked(green) #Highlight the right tile
                        
                                
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            
            for i in range(0, len(tiles), 1): # Draw tiles
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
            
            if ev.type == pygame.KEYDOWN:
                for i in range(0, len(tiles), 1):
                    tiles[i].clicked(grey)
            
            
            for i in range(0, len(tiles), 1):
                if tiles[i].tileCollidePoint(mousePos):
                    print('grey tile clicked')
            
            if ev.type == pygame.MOUSEBUTTONDOWN: # Is there a mouse event?
                for i in range(0, len(pieces)-8, 1): # Check all tiles with their indexes between 0 and 8 (red pieces)
                    if pieces[i].distFromPoints(mousePos) < pieceRadius: # Has a piece been clicked?
                        
                        #If/Elif statement to find out which diagonal the piece is on
                        if pieces[i].whichDiagonal(True) == True: #Is the piece on the "True" diagonal
                            print('true diag')
                            
                            tiles[2*i - 24].clicked(green) #Highlight tile on the right
                            
                            if (2*i + 26) < 47: #Highlight tile on the left, only if it does not go over the border
                                tiles[2*i + 26].clicked(green)
                                
                        elif pieces[i].whichDiagonal(True) == False: #Is the piece on the "False" diagonal
                            print('false diag')
                            
                            if (2*i + 23) > 47: #Highlight the tile on the right, only if it does not go over the border
                                tiles[2*i + 23].clicked(green)
                                
                            tiles[2*i + 25].clicked(green) #Highlight the left tile
                            
            mousePos = pygame.mouse.get_pos()#Mouse position for buttons
            
            #-----Drawing-----
            # So first fill everything with the background color
            mainSurface.fill((0, 0, 0))
            
            
            for i in range(0, len(tiles), 1): # Draw tiles
                tiles[i].drawTile(mainSurface)
            
            for i in range(0, len(pieces), 1): # Draw pieces
                pieces[i].drawPiece(mainSurface)
            
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower

    pygame.quit()     # Once we leave the loop, close the window.

main()