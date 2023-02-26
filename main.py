import pygame, pyautogui, pygame_menu, sys
from othello import Othello

pygame.init()
screen_width, screen_height = pyautogui.size()
base_screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.update()


def run_game():
    print("Running")
    thel = Othello()
    thel.start_game()


def quit_game():
    pygame.quit()
    sys.exit()


mainTheme = pygame_menu.Theme(
    background_color=(0, 0, 0),
    title_font_shadow=True,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
    widget_font=pygame_menu.font.FONT_HELVETICA,
    widget_font_color=(112, 131, 111),
    widget_font_size=90)

main_menu = pygame_menu.Menu("Turing Japanese, I really think so", screen_width, screen_height, theme=mainTheme)
main_menu.add.button('Start Game', run_game)
main_menu.add.button("Close", quit_game)

main_menu.mainloop(base_screen)
