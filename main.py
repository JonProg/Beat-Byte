import curses
import os
from curses import wrapper
import pygame

PATH = 'musicas'
music_names = os.listdir(PATH)

controls_select = """
      ,-----,
      |  ↑  | --Up
      '-----'
         |
      ,-----,
      |  ↓  | --Down
      '-----'

"""

controls_player = """

,-----,   ,-----,
| ←-- |---| --→ |
'-----'   '-----'
 left     right
"""
# Inicializar o Pygame
pygame.init()

# Inicializar o mixer
pygame.mixer.init()

def select_music(stdscr, selected_idx):
    stdscr.clear()
    stdscr.addstr(15,14 , controls_select)
    stdscr.addstr(17,75 , "Selecione a Música:", curses.A_BOLD)
    win_y, win_x = stdscr.getmaxyx()

    pad_width = 40
    pad_height = 15

    pad_x = (win_x // 2) - (pad_width // 2)
    pad_y = (win_y // 2) - (pad_height // 2)

    pad = curses.newpad(pad_height, pad_width)
    max_h, max_w = pad.getmaxyx()

    for idx, name in enumerate(music_names):
        name = name.replace('.mp3', '')
        if len(name)>30:
            name = name[0:30]+'...'
        x = max_w//2 - len(name)//2
        y = max_h//2 - len(music_names)//2 + idx +idx

        if idx == selected_idx:
            pad.attron(curses.color_pair(1))
            pad.addstr(y,x,name)
            pad.attroff(curses.color_pair(1))
        else:
            pad.addstr(y,x,name)
    
    stdscr.refresh()
    pad.refresh(0, 0, pad_y, pad_x, pad_y + pad_height, pad_x + pad_width)



def main(stdscr):
    curses.initscr()
    curses.curs_set(0)
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    height, width = stdscr.getmaxyx()

    current_music_idx = 0
    select_music(stdscr, current_music_idx)

    # Exiba o player de música estilizado
    #stdscr.addstr(height // 2 + 10, (width - 10) // 2, "Pressione 'q' para sair", curses.A_DIM)

    # Verifique se a tecla 'q' foi pressionada para sair

    while True:
        key = stdscr.getch()

        if key == 113:
            # Pare a música e encerre o mixer do pygame
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            break

        elif key == curses.KEY_UP and current_music_idx > 0:
            current_music_idx -= 1

        elif key == curses.KEY_DOWN and current_music_idx < len(music_names)-1:
            current_music_idx += 1

        elif key == curses.KEY_ENTER or key in [10,13]:                   

            while True:
                stdscr.clear()
                stdscr.addstr(0,0, "Tocando {}".format(music_names[current_music_idx]))
                pygame.mixer.music.load(PATH +'/{}'.format(music_names[current_music_idx]))
                pygame.mixer.music.play()

                key = stdscr.getch()

                if key == 113:
                    # Pare a música e encerre o mixer do pygame
                    break

                elif key == curses.KEY_LEFT and current_music_idx > 0:
                    current_music_idx -= 1

                elif key == curses.KEY_RIGHT and current_music_idx < len(music_names)-1:
                    current_music_idx += 1
                
                stdscr.refresh()

        select_music(stdscr, current_music_idx)

# Execute o programa
wrapper(main)
