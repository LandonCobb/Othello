import pygame as pg
import pyautogui
import sys

class Othello:
    def __init__(self):
        pg.init()
        self.screen_width, self.screen_height = pyautogui.size()      
        
        self.window = None
        
        # set up the list of cords from the text file
        self.board_cords = []
        with open("othello-assests\\board_cords.txt") as cords:
            lines = cords.readlines()
        for line in lines:
            line = line[:-1]
            line = line.split(", ")
            self.board_cords.append((int(line[0]), int(line[1])))
            
        # setup board rects
        self.board_rects = []
        count = 0
        for row in range(8):
            new_row = []
            for col in range(8):
                new_rect = pg.Rect(0, 0, 135, 135)
                new_rect.center = (self.board_cords[count][0], self.board_cords[count][1])
                new_row.append(new_rect)
                count += 1
            self.board_rects.append(new_row)

    def draw_objects(self):
        self.window.fill((255, 255, 255))
        
        board_image = pg.image.load("othello-assests\othelloboard.png")
        self.window.blit(board_image, board_image.get_rect(center = (self.screen_width // 2, self.screen_height // 2)))

        # showing hitboxes for each tile
        # for row in range(len(self.board_rects)):
        #     for col in range(len(self.board_rects[row])):
        #         pg.draw.rect(self.window, (0, 0, 0), self.board_rects[row][col])
        
    def start_game(self):
        self.window = pg.display.set_mode((self.screen_width, self.screen_height), pg.FULLSCREEN)
        pg.display.set_caption("Othello")
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    # code to easily save mouse positions #
                    # with open("cords.txt", "a") as cords:
                    #     cords.write(", ".join(map(str, event.pos)))
                    #     cords.write("\n")
                    pass

            self.draw_objects()
            pg.display.update()
            
if __name__ == "__main__":
    Othello().start_game()