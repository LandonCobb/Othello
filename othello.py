import pygame as pg
import pyautogui
import sys
from piece import Piece
import numpy as np

class Othello:
    def __init__(self):
        pg.init()
        self.screen_width, self.screen_height = pyautogui.size()      
        
        self.window = None
        
        # set up the list of cords from the text file
        board_cords = []
        with open("Othello/othello-assests/board_cords.txt") as cords:
            lines = cords.readlines()
        for line in lines:
            line = line[:-1]
            line = line.split(", ")
            board_cords.append((int(line[0]), int(line[1])))
            
        # setup board rects
        self.board_rects = []
        count = 0
        for row in range(8):
            new_row = []
            for col in range(8):
                new_rect = pg.Rect(0, 0, 135, 135)
                new_rect.center = (board_cords[count][0], board_cords[count][1])
                new_row.append(new_rect)
                count += 1
            self.board_rects.append(new_row)

        # setup pieces
        self.pieces = [[None for col in range(8)] for row in range(8)]
        self.pieces[3][3] = Piece(self.board_rects[3][3].center, (255, 255, 255))
        self.pieces[3][4] = Piece(self.board_rects[3][4].center, (0, 0, 0))
        self.pieces[4][3] = Piece(self.board_rects[4][3].center, (0, 0, 0))
        self.pieces[4][4] = Piece(self.board_rects[4][4].center, (255, 255, 255))
        self.turn = -1
        self.mayWin = False
        self.flanks = []
        self.board = np.array([[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2]])
        

    def start_game(self):
        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[3][4] = 0
        self.board[4][3] = 0
        self.window = pg.display.set_mode((self.screen_width, self.screen_height), pg.FULLSCREEN)
        pg.display.set_caption("Othello")
        # print("board: " + str(self.board))
        self.turnFun()
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    # code to easily save mouse positions for testing
                    # with open("cords.txt", "a") as cords:
                    #     cords.write(", ".join(map(str, event.pos)))
                    #     cords.write("\n")
                    collide_index = pg.Rect(event.pos[0], event.pos[1], 1, 1).collidelist([rect for row in self.board_rects for rect in row])
                    if collide_index != -1:
                        col, row = collide_index // 8, collide_index % 8
                        # print("Hit: " + str(col) + " " + str(row))
                        # add game logic
                        for x in self.flanks:
                            # print("Poss: " + str(x[0]) + " " + str(x[1]))
                            if (col == x[0] and row == x[1]):
                                positions = [[x[0], x[1]]]
                                self.flanks.clear()
                                color = (255,255,255)
                                if (self.turn%2 == 0):
                                    color = (0,0,0)
                                self.flipFlank(self.turn%2, positions)
                                self.pieces[col][row] = Piece(self.board_rects[col][row].center, color)
                                self.board[col][row] = self.turn%2
                                #  find any associating flanks and flip them
                                self.flanks.clear()
                                self.turnFun()
                        # if self.pieces[row][col] == None:
                        #     self.pieces[row][col] = Piece(self.board_rects[row][col].center, (255, 255, 255))
                        
                # testing the flipping function
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_f:
                #         for row in self.pieces:
                #             for piece in row:
                #                 if piece != None:
                #                     piece.flip()

            self.draw_objects()
            pg.display.update()
    # check if flank is possible

    def draw_objects(self):
        self.window.fill((255, 255, 255))
        
        board_image = pg.image.load("Othello\othello-assests\othelloboard.png")
        self.window.blit(board_image, board_image.get_rect(center = (self.screen_width // 2, self.screen_height // 2)))

        # showing hitboxes for each tile
        # for row in range(len(self.board_rects)):
        #     for col in range(len(self.board_rects[row])):
        #         pg.draw.rect(self.window, (0, 0, 0), self.board_rects[row][col])
        #         # for debugging showing the cords of each tile
        #         self.window.blit(pg.font.Font(None, 30).render(f"{row}, {col}", True, (255, 255, 255)), self.board_rects[row][col].center)

        for row in self.pieces:
            for piece in row:
                if piece != None:
                    pg.draw.circle(self.window, piece.color, piece.center, 50)

    def flipFlank(self, checkVal, positions):
        # find flanks
        # for each in positions
        # check each path for if it finds a two without passing over an anti
        color = (255,255,255)
        if (self.turn%2 == 0):
            color = (0,0,0)
        addCheck = 0
        for a in positions:
            anti = 0
            if (checkVal == 0):
                anti = 1
            # up
            if(self.board[a[0]-1][a[1]] == anti):
                valOfUse1 = a[0]-1
                while (valOfUse1 >= 0):
                    if (self.board[valOfUse1][a[1]] == 2):
                        break
                    elif (self.board[valOfUse1][a[1]] == checkVal):
                        valOfUse1 += 1
                        while valOfUse1 < a[0]:
                            self.pieces[valOfUse1][a[1]] = Piece(self.board_rects[valOfUse1][a[1]].center, color)
                            self.board[valOfUse1][a[1]] = checkVal
                            valOfUse1 += 1
                        break
                    valOfUse1 -= 1
            # down
            if(self.board[a[0]+1][a[1]] == anti):
                valOfUse1 = a[0]+1
                while (valOfUse1 <= 7):
                    if (self.board[valOfUse1][a[1]] == 2):
                        break
                    elif (self.board[valOfUse1][a[1]] == checkVal):
                        valOfUse1 -= 1
                        while valOfUse1 > a[0]:
                            self.pieces[valOfUse1][a[1]] = Piece(self.board_rects[valOfUse1][a[1]].center, color)
                            self.board[valOfUse1][a[1]] = checkVal
                            valOfUse1 -= 1
                        break
                    valOfUse1 += 1
            # left
            if(self.board[a[0]][a[1]-1] == anti):
                valOfUse1 = a[1]-1
                while (valOfUse1 >= 0):
                    if (self.board[a[0]][valOfUse1] == 2):
                        break
                    elif (self.board[a[0]][valOfUse1] == checkVal):
                        valOfUse1 += 1
                        while valOfUse1 < a[1]:
                            self.pieces[a[0]][valOfUse1] = Piece(self.board_rects[a[0]][valOfUse1].center, color)
                            self.board[a[0]][valOfUse1] = checkVal
                            valOfUse1 += 1
                        break
                    valOfUse1 -= 1
            # right
            if(self.board[a[0]][a[1]+1] == anti):
                valOfUse1 = a[1]+1
                while (valOfUse1 <= 7):
                    if (self.board[a[0]][valOfUse1] == 2):
                        break
                    elif (self.board[a[0]][valOfUse1] == checkVal):
                        valOfUse1 -= 1
                        while valOfUse1 > a[1]:
                            self.pieces[a[0]][valOfUse1] = Piece(self.board_rects[a[0]][valOfUse1].center, color)
                            self.board[a[0]][valOfUse1] = checkVal
                            valOfUse1 -= 1
                        break
                    valOfUse1 += 1
            # diagon ne
            if(self.board[a[0]-1][a[1]+1] == anti):
                valOfUse1 = a[0]-1
                valOfUse2 = a[1]+1
                while (valOfUse1 >= 0 and valOfUse2 <= 7):
                    if (self.board[valOfUse1][valOfUse2] == 2):
                        break
                    elif (self.board[valOfUse1][valOfUse2] == checkVal):
                        valOfUse1 += 1
                        valOfUse2 -= 1
                        while valOfUse1 < a[0] and valOfUse2 > a[1]:
                            self.pieces[valOfUse1][valOfUse2] = Piece(self.board_rects[valOfUse1][valOfUse2].center, color)
                            self.board[valOfUse1][valOfUse2] = checkVal
                            valOfUse1 += 1
                            valOfUse2 -= 1
                        break
                    valOfUse1 -= 1
                    valOfUse2 += 1
            # diagon se
            if(self.board[a[0]+1][a[1]+1] == anti):
                valOfUse1 = a[0]+1
                valOfUse2 = a[1]+1
                while (valOfUse1 <= 7 and valOfUse2 <= 7):
                    if (self.board[valOfUse1][valOfUse2] == 2):
                        break
                    elif (self.board[valOfUse1][valOfUse2] == checkVal):
                        valOfUse1 -= 1
                        valOfUse2 -= 1
                        while valOfUse1 > a[0] and valOfUse2 > a[1]:
                            self.pieces[valOfUse1][valOfUse2] = Piece(self.board_rects[valOfUse1][valOfUse2].center, color)
                            self.board[valOfUse1][valOfUse2] = checkVal
                            valOfUse1 -= 1
                            valOfUse2 -= 1
                        break
                    valOfUse1 += 1
                    valOfUse2 += 1
            # diagon sw
            if(self.board[a[0]+1][a[1]-1] == anti):
                valOfUse1 = a[0]+1
                valOfUse2 = a[1]-1
                while (valOfUse1 <= 7 and valOfUse2 >= 0):
                    if (self.board[valOfUse1][valOfUse2] == 2):
                        break
                    elif (self.board[valOfUse1][valOfUse2] == checkVal):
                        valOfUse1 -= 1
                        valOfUse2 += 1
                        while valOfUse1 > a[0] and valOfUse2 < a[1]:
                            self.pieces[valOfUse1][valOfUse2] = Piece(self.board_rects[valOfUse1][valOfUse2].center, color)
                            self.board[valOfUse1][valOfUse2] = checkVal
                            valOfUse1 -= 1
                            valOfUse2 += 1
                        break
                    valOfUse1 += 1
                    valOfUse2 -= 1
            # diagon nw
            if(self.board[a[0]-1][a[1]-1] == anti):
                valOfUse1 = a[0]-1
                valOfUse2 = a[1]-1
                while (valOfUse1 >= 0 and valOfUse2 >= 0):
                    if (self.board[valOfUse1][valOfUse2] == 2):
                        break
                    elif (self.board[valOfUse1][valOfUse2] == checkVal):
                        valOfUse1 += 1
                        valOfUse2 += 1
                        while valOfUse1 < a[0] and valOfUse2 < a[1]:
                            self.pieces[valOfUse1][valOfUse2] = Piece(self.board_rects[valOfUse1][valOfUse2].center, color)
                            self.board[valOfUse1][valOfUse2] = checkVal
                            valOfUse1 += 1
                            valOfUse2 += 1
                        break
                    valOfUse1 -= 1
                    valOfUse2 -= 1

    def checkFlank(self, checkVal, positions):
        # find flanks
        print(checkVal)
        print(self.board)
        # for each in positions
        # check each path for if it finds a two without passing over an anti
        addCheck = 0
        for a in positions:
            anti = 0
            if (checkVal == 0):
                anti = 1
            # up
            if(self.board[a[0]-1][a[1]] == anti):
                valOfUse1 = a[0]-1
                while (valOfUse1 >= 0):
                    if (self.board[valOfUse1][a[1]] == 2):
                        addCheck += 1
                        self.flanks.append([valOfUse1, a[1]])
                        break
                    elif (self.board[valOfUse1][a[1]] == checkVal):
                        break
                    valOfUse1 -= 1
            # down
            if(self.board[a[0]+1][a[1]] == anti):
                valOfUse1 = a[0]+1
                while (valOfUse1 <= 7):
                    if (self.board[valOfUse1][a[1]] == 2):
                        addCheck += 1
                        self.flanks.append([valOfUse1, a[1]])
                        break
                    elif (self.board[valOfUse1][a[1]] == checkVal):
                        break
                    valOfUse1 += 1
            # left
            if(self.board[a[0]][a[1]-1] == anti):
                valOfUse1 = a[1]-1
                while (valOfUse1 >= 0):
                    if (self.board[a[0]][valOfUse1] == 2):
                        addCheck += 1
                        self.flanks.append([a[0], valOfUse1])
                        break
                    elif (self.board[a[0]][valOfUse1] == checkVal):
                        break
                    valOfUse1 -= 1
            # right
            if(self.board[a[0]][a[1]+1] == anti):
                valOfUse1 = a[1]+1
                while (valOfUse1 <= 7):
                    if (self.board[a[0]][valOfUse1] == 2):
                        addCheck += 1
                        self.flanks.append([a[0], valOfUse1])
                        break
                    elif (self.board[a[0]][valOfUse1] == checkVal):
                        break
                    valOfUse1 += 1
            # diagon ne
            if(self.board[a[0]-1][a[1]+1] == anti):
                valOfUse1 = a[0]-1
                valOfUse2 = a[1]+1
                while (valOfUse1 >= 0 and valOfUse2 <= 7):
                    if (self.board[valOfUse1][valOfUse2] == 2):
                        addCheck += 1
                        self.flanks.append([valOfUse1, valOfUse2])
                        break
                    elif (self.board[valOfUse1][valOfUse2] == checkVal):
                        break
                    valOfUse1 -= 1
                    valOfUse2 += 1
            # diagon se
            if(self.board[a[0]+1][a[1]+1] == anti):
                valOfUse1 = a[0]+1
                valOfUse2 = a[1]+1
                while (valOfUse1 <= 7 and valOfUse2 <= 7):
                    if (self.board[valOfUse1][valOfUse2] == 2):
                        addCheck += 1
                        self.flanks.append([valOfUse1, valOfUse2])
                        break
                    elif (self.board[valOfUse1][valOfUse2] == checkVal):
                        break
                    valOfUse1 += 1
                    valOfUse2 += 1
            # diagon sw
            if(self.board[a[0]+1][a[1]-1] == anti):
                valOfUse1 = a[0]+1
                valOfUse2 = a[1]-1
                while (valOfUse1 <= 7 and valOfUse2 >= 0):
                    if (self.board[valOfUse1][valOfUse2] == 2):
                        addCheck += 1
                        self.flanks.append([valOfUse1, valOfUse2])
                        break
                    elif (self.board[valOfUse1][valOfUse2] == checkVal):
                        break
                    valOfUse1 += 1
                    valOfUse2 -= 1
            # diagon nw
            if(self.board[a[0]-1][a[1]-1] == anti):
                valOfUse1 = a[0]-1
                valOfUse2 = a[1]-1
                while (valOfUse1 >= 0 and valOfUse2 >= 0):
                    if (self.board[valOfUse1][valOfUse2] == 2):
                        addCheck += 1
                        self.flanks.append([valOfUse1, valOfUse2])
                        break
                    elif (self.board[valOfUse1][valOfUse2] == checkVal):
                        break
                    valOfUse1 -= 1
                    valOfUse2 -= 1

        # mark current flanks as red and remove old flanks
        # could put flanks as a draw object item
        # return number of flanks possible
        return addCheck
    # black first
    # present placements in arraylist [l,l] spots
    # if no flank is possible next persons turn

    def turnFun(self):
        self.turn += 1
        if (self.turn % 2 == 0):
            # check black
            positions = list(zip(*np.where(self.board == 0)))
            print(positions)
            available = self.checkFlank(0, positions)
            if (available > 0):
                self.mayWin = False
            elif (not self.mayWin):
                self.mayWin = True
                self.turnFun()
            else:
                self.gameEnd()
        elif (self.turn % 2 == 1):
            # check white
            positions = list(zip(*np.where(self.board == 1)))
            print(positions)
            available = self.checkFlank(1, positions)
            if (available > 0):
                self.mayWin = False
            elif (not self.mayWin):
                self.mayWin = True
                self.turnFun()
            else:
                self.gameEnd()
    # go until all spots are full or both cannot flank

    def gameEnd(self):
        # count both sides
        white = 0
        black = 0
        for a in self.board:
            for b in a:
                if (b == 1):
                    white += 1
                elif (b == 0):
                    black += 1
        if (black > white):
            pass
        elif (white > black):
            pass
        else:
            # tie
            pass
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    Othello().start_game()