import pygame as pg
import pyautogui
import sys
from piece import Piece

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
        
    def start_game(self):
        self.window = pg.display.set_mode((self.screen_width, self.screen_height), pg.FULLSCREEN)
        pg.display.set_caption("Othello")
        
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
                        row, col = collide_index // 8, collide_index % 8
                        # add game logic
                        if self.pieces[row][col] == None:
                            self.pieces[row][col] = Piece(self.board_rects[row][col].center, (255, 255, 255))
                        
                # testing the flipping function
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_f:
                #         for row in self.pieces:
                #             for piece in row:
                #                 if piece != None:
                #                     piece.flip()

            self.draw_objects()
            pg.display.update()
            
if __name__ == "__main__":
    Othello().start_game()