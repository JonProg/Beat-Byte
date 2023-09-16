import curses
import pygame
import os

from pyfiglet import figlet_format
from curses import wrapper


PATH = 'musicas'
music_names = os.listdir(PATH)


title = figlet_format("Beat-Byte", font = "big")

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
                                                                      | <-- |---| --> |
                                                                      '-----'   '-----'
                                                                       left     right
"""

# Inicializar o Pygame  
pygame.init()

# Inicializar o mixer
pygame.mixer.init()

pad_width = 40
pad_height = 15

def select_music(stdscr, selected_idx, pad):
    stdscr.clear()
    pad.clear()
    win_y, win_x = stdscr.getmaxyx()

    pad_x = (win_x // 2) - (pad_width // 2) 
    pad_y = (win_y // 2) - (pad_height // 2) + 3

    max_h, max_w = pad.getmaxyx()

    if music_names == []:
        stdscr.addstr(win_y // 2 - 8, win_x // 2 - 10, "Nenhuma música encontrada", curses.A_BOLD)
        return pad.refresh(0, 0, pad_y, pad_x, pad_y + pad_height, pad_x + pad_width)


    stdscr.addstr(1, 0, title)
    stdscr.addstr(win_y // 2 - 8, win_x // 2 - 10, "Selecione a Música:", curses.A_BOLD)
    stdscr.addstr(win_y // 2 + 13, win_x // 2 - 10, "Aperte 'Q' para sair")
    stdscr.addstr(win_y // 2 - 4, win_x // 2, controls_select)

    for idx, name in enumerate(music_names[selected_idx:selected_idx+pad_height]):
        name = name.replace('.mp3', '')
        if len(name)>30:
            name = name[0:30]+'...'

        if idx == 0:
            pad.attron(curses.color_pair(1))
            pad.addstr(idx,3,name)
            pad.attroff(curses.color_pair(1))
        else:
            pad.addstr(idx,2,name)
    
    stdscr.refresh()
    pad.refresh(0, 0, pad_y, pad_x, pad_y + pad_height, pad_x + pad_width)

def main(stdscr):
    curses.initscr()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    pad = curses.newpad(pad_height, pad_width)

    current_music_idx = 0
    select_music(stdscr, current_music_idx, pad)

    while True:
        key = stdscr.getch()

        # Verifique se a tecla 'q' foi pressionada para sair
        if key in [113, 81]:
            # Pare a música e encerre o mixer do pygame
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            break

        elif key == curses.KEY_UP and current_music_idx > 0:
            current_music_idx -= 1

        elif key == curses.KEY_DOWN and current_music_idx < len(music_names) -1:
            current_music_idx += 1

        elif key == curses.KEY_ENTER or key in [10,13]:                   
            while True:
                stdscr.clear()
                name_music = music_names[current_music_idx].replace('.mp3', '')
                if len(music_names[current_music_idx])>30:
                    name_music = music_names[current_music_idx][0:30]+'...'

                height, width = stdscr.getmaxyx()

                try:
                    pygame.mixer.music.load(PATH +'/{}'.format(music_names[current_music_idx]))
                    pygame.mixer.music.play()

                    if current_music_idx < len(music_names) - 1:
                        pygame.mixer.music.queue(PATH +'/{}'.format(music_names[current_music_idx + 1]))

                    valid = True

                except pygame.error:
                    stdscr.addstr(height // 2  - 5, (width - 60) // 2 , "Arquivo MP3 corronpido (-_-*). Volte e coloque outra música")
                    valid = False
                
                if valid:
                    stdscr.addstr(height // 2  - 5, (width - 40) // 2, name_music)
                    stdscr.addstr(height // 2  - 3, (width - 40) // 2 , controls_player)

                stdscr.addstr(height // 2 + 5, (width - 40) // 2 + 5, "Aperte 'Q' para voltar", curses.A_BOLD)

                stdscr.refresh()

                key = stdscr.getch()

                if key in [113, 81]:
                    # Pare a música e encerre o mixer do pygame
                    break

                elif key == curses.KEY_LEFT and current_music_idx > 0:
                    current_music_idx -= 1

                elif key == curses.KEY_RIGHT and current_music_idx < len(music_names)-1:
                    current_music_idx += 1
                
        select_music(stdscr, current_music_idx, pad)

# Execute o programa
wrapper(main)
