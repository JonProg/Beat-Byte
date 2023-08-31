import curses
import os
from curses import wrapper
import pygame

PATH = 'musicas'
music_names = os.listdir(PATH)

def main(stdscr):
    # Configuração inicial do curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Inicialização do mixer do pygame
    pygame.mixer.init()

    # Carregue a música
    pygame.mixer.music.load(r'musicas\bryson tiller - dont (sped up).mp3')

    # Reproduza a música
    pygame.mixer.music.play()

    # Loop principal
    while True:
        # Limpe a tela
        stdscr.clear()

        # Obtenha o tamanho da tela
        height, width = stdscr.getmaxyx()
        pad_music = curses.newpad(1,50)
 
        # Exiba o player de música estilizado
        stdscr.addstr(height // 2, (width - 10) // 2, "Player de Música", curses.A_BOLD)
        stdscr.addstr(height // 2 + 2, (width - 10) // 2, "Pressione 'q' para sair", curses.A_DIM)

        # Atualize a tela
        stdscr.refresh()

        for name in music_names:
            pad_music.addstr(name)
        
        #pad.refresh(0,0,5,5,25,25)

        # Verifique se a tecla 'q' foi pressionada para sair
        key = stdscr.getch()
        if key == ord('q'):
            break

    # Pare a música e encerre o mixer do pygame
    pygame.mixer.music.stop()
    pygame.mixer.quit()

# Execute o programa
wrapper(main)
