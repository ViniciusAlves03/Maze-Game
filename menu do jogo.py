import pygame , sys
pygame.init()

def menu (janela,wallpaper):
    pygame.font.init()
    fonte_base      = pygame.font.SysFont("Arial",110)
    str_jogador     = ''
    ContadorLetras  = 4

    def wallpaper_changer (num_wallpaper):
        fundo = pygame.image.load('menu_labirinto/wallpaper{}.png'.format(num_wallpaper))
        return fundo

    while janela != 0:
        janela.blit (wallpaper_changer(wallpaper),(0,0))
        pygame.time.delay(60)

        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and wallpaper == 3 and ContadorLetras > 0:
                str_jogador = str_jogador.upper()

                if event.key == pygame.K_BACKSPACE:
                    str_jogador = str_jogador[:-1]
                    ContadorLetras += 1

                elif ContadorLetras > 1:
                    str_jogador += event.unicode
                    ContadorLetras -= 1
                    str_jogador = str_jogador.upper()

                elif event.key == pygame.K_SPACE and len(str_jogador) == 3:
                    return str_jogador

        text_surface = fonte_base.render(str_jogador,True,(255,255,255))
        comando = pygame.key.get_pressed()

        if   wallpaper == 0 and comando[pygame.K_SPACE] : wallpaper = 1
        elif wallpaper == 1 and comando[pygame.K_UP]    : wallpaper = 3
        elif wallpaper == 1 and comando[pygame.K_SPACE] : wallpaper = 1
        elif wallpaper == 1 and comando[pygame.K_DOWN]  : wallpaper = 2
        elif wallpaper == 2 and comando[pygame.K_SPACE] : wallpaper = 1
        elif wallpaper == 3                             : janela.blit(text_surface,(160,185))

        pygame.display.update()

menu(pygame.display.set_mode ((500,550)),0)