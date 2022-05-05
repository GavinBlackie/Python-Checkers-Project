#-----------------------------------------------------------------------------
# Name:        Assignment Template (assignment.py)
# Purpose:     A description of your program goes here.
#
# Author:      Gavin B.
# Created:     04-May-2022
# Updated:     13-Sept-2020
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

    
def main():
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 720   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
    #--Variables--
    programState = 'Player 1 Turn'
    
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
    
    #--Object Classes--
    class buttonTile(): #Class object for tiles and buttons
        def __init__(self, inputColour, inputRect):
            self.rect = inputRect
            self.colour = inputColour
            
        def drawTile(self, inputSurface):
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
     
    class piece():
        def __init__(self, inputColour, inputPos, inputRadius):
            self.pos = inputPos
            self.colour = inputColour
            self.radius = inputRadius
            
        def drawPiece(self, inputSurface):
            pygame.draw.circle(inputSurface, self.colour, self.pos, self.radius)
        
    
    
    
    #------Object Definitions------
    
    
    #--Tiles--
    
    tiles = [] # List of tiles/tile information for the program to draw from
    
    # Load Tile Format into tiles list using for loops
    for y in range(0, 8, 1): #For loop that repeats 8 times, the number of rows
        
        for x in range(0, 8, 1): #For loop that repeats 8 times, the number of columns
            if isTileWhite == True: # Add a white tile if True
                tiles.append(buttonTile( white, [tilePos[0], tilePos[1], tileWidth, tileHeight] ))
                tilePos[0] += tileWidth
            elif isTileWhite == False: # Add a red tile if False
                tiles.append(buttonTile( grey, [tilePos[0], tilePos[1], tileWidth, tileHeight] ))
                tilePos[0] += tileWidth
            isTileWhite = not isTileWhite # Alternate the colour along the x axis
            
        tilePos[1] += tileHeight #Add the y for the next line of tiles
        tilePos[0] -= tileWidth*8 # Decrease the x of the tiles by 8 times the width of one tile (the length of the board)
        isTileWhite = not isTileWhite # Alternate the colour along the y axis (create grid pattern instead of straight red & white lines)
    
    #--Pieces--
    
    pieces = []
    
    for x in range(0, 4, 1):
        pieces.append(piece (red, piecePos, pieceRadius) )
        piecePos[0] += 36
    
        print(piecePos)
    
    while True:
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
        
        
        if programState == 'Player 1 Turn':
            
            # Update your game objects and data structures here...
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0, len(tiles), 1):
                    if tiles[i].tileCollidePoint(mousePos):
                        print('aaaaaaaaaa')
                        
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