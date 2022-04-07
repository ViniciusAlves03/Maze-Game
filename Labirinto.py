import time, pygame, os, sys, sqlite3
from random import randint
from pygame.constants import MOUSEBUTTONDOWN, QUIT

# inicializa todos os módulos que necessitam de inicialização dentro do pygame.
pygame.init()

#Criando conexão com o banco de dados e definindo o cursor:
banco_de_dados = sqlite3.connect('nome_pontuacao.db')
cursor = banco_de_dados.cursor() #Objeto que vai permitir realizar alterações no banco de dados


#Vai atribuir a variável 'itens' os 10 primeiros registros do banco de dados
itens1 = cursor.fetchmany(10)

# Criar a janela
janela = pygame.display.set_mode((500, 550))

clock = pygame.time.Clock()

#Variável que vai armazenar o nome do jogador temporariamente:
nome = ""

#Criar variável que vai armazenar a soma dos tempos de todos os mapas (Pontuação)
pontos = 0

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

# Mudar o título do jogo
pygame.display.set_caption('Maze and Cannons')
icone = pygame.image.load(os.path.join(diretorio_imagens, 'lab.png')) # imagem deve estar no diretório onde se encontra o programa
pygame.display.set_icon(icone)

# Carregando sons
musicatema = pygame.mixer.music.load(os.path.join(diretorio_sons, 'enter.mp3'))
pygame.mixer.music.set_volume(0.08)
pygame.mixer.music.play(-1)

somtiro = pygame.mixer.Sound(os.path.join(diretorio_sons, 'tiro1.mp3'))
somtiro.set_volume(0.1)

somDano = pygame.mixer.Sound(os.path.join(diretorio_sons, 'dano.mp3'))

somGameOver = pygame.mixer.Sound(os.path.join(diretorio_sons, 'somGameOver.mp3'))

somClick = pygame.mixer.Sound(os.path.join(diretorio_sons, 'click.mp3'))
somClick.set_volume(0.1)

somChegada = pygame.mixer.Sound(os.path.join(diretorio_sons, 'somchegada.mp3'))
somChegada.set_volume(0.1)


# Definindo cores
preto = (0,0,0)
branco = (255,255,255)
verdelimao = (15, 255, 149)
vermelho = (255, 49, 46)
azul = (72, 172, 240)
rosa = (252, 24, 152)
amarelo = (252,252,4)
fonte = pygame.font.Font("Gamer.ttf",40)
espessura = 9

# Criar a janela
largura_janela = 500
altura_janela = 550

#Criação dos botões Continuar e sair:
class Botão:
    def __init__(self,texto,largura_botão,altura_botão,posição):

        #Atributos principais:
        self.pressed = False
        #Retângulo superior:
        self.top_rect = pygame.Rect(posição,(largura_botão,altura_botão))
        self.top_color = '#475F77'

        #Segundo retângulo:
        self.bottom_rect = pygame.Rect(posição,(largura_botão,altura_botão))
        self.bottom_color = '#354B5E'

        #texto do botão:
        self.text_surf = fonte.render(texto,True,branco)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    #Função para desenhar o botão:
    def desenhar_botão(self):
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        

        pygame.draw.rect(janela,self.bottom_color,self.bottom_rect,border_radius = 12)
        pygame.draw.rect(janela,self.top_color,self.top_rect,border_radius = 15)
        janela.blit(self.text_surf,self.text_rect)
        self.checar_click()
    
    #Função para verficar o click no botão:
    def checar_click(self):
        posição_mouse = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(posição_mouse):
            self.top_color = vermelho
        
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
        
            else:
                if self.pressed == True:
                    self.pressed = False
        else:
            self.top_color = azul

#Função referente a tela de Ranking:
def tela_rank(largura_janela,altura_janela):
    janela_rank = pygame.display.set_mode((largura_janela, altura_janela))
    fonte_ranking = pygame.font.Font('Gamer.ttf', 80)
    fonte_ranking2 = pygame.font.Font('Gamer.ttf', 40)
    sair = False
    while sair == False:
        mensagem_ranking = "HIGH SCORES"
        texto_ranking = fonte_ranking.render(mensagem_ranking,True,(vermelho))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                sair = True   

            #Verifando se houve clique no botão Continuar:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                #Verificando se houve clique no botão Sair:
                if x > 170 and y > 510 and x < 330 and y < 540:
                    sair = True 


        #Inserindo texto de rank, score e nome:
        mensagem_rank = "RANK"
        texto_rank = fonte_ranking2.render(mensagem_rank,True,(amarelo))

        mensagem_score = "SCORE"
        texto_score = fonte_ranking2.render(mensagem_score,True,(amarelo))

        mensagem_name = "NAME"
        texto_name = fonte_ranking2.render(mensagem_name,True,(amarelo))

        #Textos das posições:
        mensagem_posição1 = "1ST"
        texto_posição1 = fonte_ranking2.render(mensagem_posição1,True,(branco))

        mensagem_posição2 = "2ND"
        texto_posição2 = fonte_ranking2.render(mensagem_posição2,True,(vermelho))

        mensagem_posição3 = "3RD"
        texto_posição3 = fonte_ranking2.render(mensagem_posição3,True,(amarelo))

        mensagem_posição4 = "4TH"
        texto_posição4 = fonte_ranking2.render(mensagem_posição4,True,(amarelo))

        mensagem_posição5 = "5TH"
        texto_posição5 = fonte_ranking2.render(mensagem_posição5,True,(verdelimao))

        mensagem_posição6 = "6TH"
        texto_posição6 = fonte_ranking2.render(mensagem_posição6,True,(azul))

        mensagem_posição7 = "7TH"
        texto_posição7 = fonte_ranking2.render(mensagem_posição7,True,(azul))

        mensagem_posição8 = "8TH"
        texto_posição8 = fonte_ranking2.render(mensagem_posição8,True,(vermelho))

        mensagem_posição9 = "9TH"
        texto_posição9 = fonte_ranking2.render(mensagem_posição9,True,(branco))

        mensagem_posição10 = "10TH"
        texto_posição10 = fonte_ranking2.render(mensagem_posição10,True,(rosa))

        #Textos dos scores:
        mensagem_score1 = str(itens1[0][1])
        texto_score1 = fonte_ranking2.render(mensagem_score1,True,(branco))

        
        mensagem_score2 = str(itens1[1][1])
        texto_score2 = fonte_ranking2.render(mensagem_score2,True,(vermelho))

        
        mensagem_score3 = str(itens1[2][1])
        texto_score3 = fonte_ranking2.render(mensagem_score3,True,(amarelo))

        
        
        mensagem_score4 = str(itens1[3][1])
        texto_score4 = fonte_ranking2.render(mensagem_score4,True,(amarelo))

        
        mensagem_score5 = str(itens1[4][1])
        texto_score5 = fonte_ranking2.render(mensagem_score5,True,(verdelimao))

        
        mensagem_score6 = str(itens1[5][1])
        texto_score6 = fonte_ranking2.render(mensagem_score6,True,(azul))

        
        mensagem_score7 = str(itens1[6][1])
        texto_score7 = fonte_ranking2.render(mensagem_score7,True,(azul))

        
        mensagem_score8 = str(itens1[7][1])
        texto_score8 = fonte_ranking2.render(mensagem_score8,True,(vermelho))

        
        mensagem_score9 = str(itens1[8][1])
        texto_score9 = fonte_ranking2.render(mensagem_score9,True,(branco))
        
        
        mensagem_score10 = str(itens1[9][1])
        texto_score10 = fonte_ranking2.render(mensagem_score10,True,(rosa))

        #Textos dos nomes:
        mensagem_nome1 = itens1[0][2]
        texto_nome1 = fonte_ranking2.render(mensagem_nome1,True,(branco))

        mensagem_nome2 = itens1[1][2]
        texto_nome2 = fonte_ranking2.render(mensagem_nome2,True,(vermelho))

        mensagem_nome3 = itens1[2][2]
        texto_nome3 = fonte_ranking2.render(mensagem_nome3,True,(amarelo))

        mensagem_nome4 = itens1[3][2]
        texto_nome4 = fonte_ranking2.render(mensagem_nome4,True,(amarelo))

        mensagem_nome5 = itens1[4][2]
        texto_nome5 = fonte_ranking2.render(mensagem_nome5,True,(verdelimao))

        mensagem_nome6 = itens1[5][2]
        texto_nome6 = fonte_ranking2.render(mensagem_nome6,True,(azul))

        mensagem_nome7 = itens1[6][2]
        texto_nome7 = fonte_ranking2.render(mensagem_nome7,True,(azul))

        mensagem_nome8 = itens1[7][2]
        texto_nome8 = fonte_ranking2.render(mensagem_nome8,True,(vermelho))

        mensagem_nome9 = itens1[8][2]
        texto_nome9 = fonte_ranking2.render(mensagem_nome9,True,(branco))

        mensagem_nome10 = itens1[9][2]
        texto_nome10 = fonte_ranking2.render(mensagem_nome10,True,(rosa))


        #botão_continuar.desenhar_botão() REVER
        botão_sair.desenhar_botão()

        #Desenhar tabelas do rank:
        janela_rank.blit(texto_rank,(70,100))
        janela_rank.blit(texto_score,(210,100))
        janela_rank.blit(texto_name,(350,100))
        janela_rank.blit(texto_ranking,(90,0))

        #Desenhar números referentes a cada posição:
        janela_rank.blit(texto_posição1,(75,140))
        janela_rank.blit(texto_posição2,(75,170))
        janela_rank.blit(texto_posição3,(75,200))
        janela_rank.blit(texto_posição4,(75,230))
        janela_rank.blit(texto_posição5,(75,260))
        janela_rank.blit(texto_posição6,(75,290))
        janela_rank.blit(texto_posição7,(75,320))
        janela_rank.blit(texto_posição8,(75,350))
        janela_rank.blit(texto_posição9,(75,380))
        janela_rank.blit(texto_posição10,(75,410))

        #Desenhar scores:
        janela_rank.blit(texto_score1,(240,140))
        janela_rank.blit(texto_score2,(240,170))
        janela_rank.blit(texto_score3,(240,200))
        janela_rank.blit(texto_score4,(240,230))
        janela_rank.blit(texto_score5,(240,260))
        janela_rank.blit(texto_score6,(240,290))
        janela_rank.blit(texto_score7,(240,320))
        janela_rank.blit(texto_score8,(240,350))
        janela_rank.blit(texto_score9,(240,380))
        janela_rank.blit(texto_score10,(240,410))

        #Desenhar nomes:
        janela_rank.blit(texto_nome1,(360,140))
        janela_rank.blit(texto_nome2,(360,170))
        janela_rank.blit(texto_nome3,(360,200))
        janela_rank.blit(texto_nome4,(360,230))
        janela_rank.blit(texto_nome5,(360,260))
        janela_rank.blit(texto_nome6,(360,290))
        janela_rank.blit(texto_nome7,(360,320))
        janela_rank.blit(texto_nome8,(360,350))
        janela_rank.blit(texto_nome9,(360,380))
        janela_rank.blit(texto_nome10,(360,410))
        
        pygame.display.flip() # atualiza a tela 
        clock.tick(60)
    
    return janela_rank

#Criando instância da classe Botão:
botão_sair = Botão("Sair",160,30,(170,510))  

def criarCanhão(imagem ,x, y):
    janela.blit(imagem, (x, y))

def criarCoracao(imagem, x, y):
    janela.blit(imagem, (x, y))

def desenharMapa(mapa, x, y):
    janela.blit(mapa, (x, y))

def drawBarreirasLimitadoras(cor):
    pygame.draw.line(janela, cor, [16,20], [484,20], espessura) # barra horizontal superior
    pygame.draw.line(janela, cor, [20,20], [20, 480], espessura) # barra na vertical esquerda
    pygame.draw.line(janela, cor, [480,20], [480,480], espessura) # barra vertical direita
    pygame.draw.line(janela, cor, [16,480], [484,480], espessura) # barra horizontal inferior

def drawCoracaoHud():
    criarCoracao(coracaoImagem1, coracao1X, coracao1Y)
    criarCoracao(coracaoImagem2, coracao2X, coracao2Y)
    criarCoracao(coracaoImagem3, coracao3X, coracao3Y)
    criarCoracao(coracaoImagem4, coracao4X, coracao4Y)
    criarCoracao(coracaoImagem5, coracao5X, coracao5Y)

# Carregando fonte do jogo
fonte = pygame.font.Font('Gamer.ttf', 55)

# imagem de coração
coracaoImagem1 = pygame.image.load(os.path.join(diretorio_imagens, 'coracao.png'))
coracaoImagem1 = pygame.transform.scale(coracaoImagem1, (36, 36))

coracao1X = 10
coracao1Y = 500

coracaoImagem2 = pygame.image.load(os.path.join(diretorio_imagens, 'coracao.png'))
coracaoImagem2 = pygame.transform.scale(coracaoImagem2, (36, 36))

coracao2X = 46
coracao2Y = 500

coracaoImagem3 = pygame.image.load(os.path.join(diretorio_imagens, 'coracao.png'))
coracaoImagem3 = pygame.transform.scale(coracaoImagem3, (36, 36))

coracao3X = 82
coracao3Y = 500

coracaoImagem4 = pygame.image.load(os.path.join(diretorio_imagens, 'coracao.png'))
coracaoImagem4 = pygame.transform.scale(coracaoImagem4, (36, 36))

coracao4X = 118
coracao4Y = 500

coracaoImagem5 = pygame.image.load(os.path.join(diretorio_imagens, 'coracao.png'))
coracaoImagem5 = pygame.transform.scale(coracaoImagem5, (36, 36))

coracao5X = 154
coracao5Y = 500
#----------------------------------------------------------------------------------------------
# imagem do canhão
canhaoImagem = pygame.image.load(os.path.join(diretorio_imagens, 'canhao.png'))
canhaoImagem = pygame.transform.scale(canhaoImagem, (24, 24))
canhaoImagem = pygame.transform.flip(canhaoImagem, True, False)

canhaoImagem2 = pygame.image.load(os.path.join(diretorio_imagens, 'canhao.png'))
canhaoImagem2 = pygame.transform.scale(canhaoImagem2, (24, 24))
canhaoImagem2 = pygame.transform.flip(canhaoImagem2, True, False)

canhaoImagem3 = pygame.image.load(os.path.join(diretorio_imagens, 'canhao.png'))
canhaoImagem3 = pygame.transform.scale(canhaoImagem3, (24, 24))


# posição do canhão 1
canhao1X = 475
canhao1Y = 100

# bala canhao 1
bala1X = canhao1X
bala1Y = canhao1Y + 8
bala1MudançaX = 0
bala1MudançaY = 0
tempoBala1 = randint(1,3)
auxTempoBala1 = -tempoBala1

# posição do canhão 2
canhao2X = 475
canhao2Y = 225

# bala canhao 2
bala2X = canhao2X
bala2Y = canhao2Y + 8
bala2MudançaX = 0
bala2MudançaY = 0
tempoBala2 = randint(1,3)
auxTempoBala2 = -tempoBala2

# posição do canhão 3
canhao3X = 475
canhao3Y = 350

# bala canhao 3
bala3X = canhao3X
bala3Y = canhao3Y + 8
bala3MudançaX = 0
bala3MudançaY = 0
tempoBala3 = randint(1,3)
auxTempoBala3 = -tempoBala3

#velocidade das balas dos canhões
velocidadeBala = 9
#-----------------------------------------------------------------------------------------------


# imagem do mapa 1
mapa1 = pygame.image.load(os.path.join(diretorio_imagens, 'mapa.png'))
mapa1 = pygame.transform.scale(mapa1, (510, 510))


# imagem do mapa 2
mapa2 = pygame.image.load(os.path.join(diretorio_imagens, 'mapa2.png'))
mapa2 = pygame.transform.scale(mapa2, (520, 460))

# imagem do mapa 3
mapa3 = pygame.image.load(os.path.join(diretorio_imagens, 'mapa3.png'))
mapa3 = pygame.transform.scale(mapa3, (465, 465))

# imagem da tela de game over
gameoverImagem = pygame.image.load(os.path.join(diretorio_imagens, 'Game_Over.png'))


# Posição da chegada
chegadaX = 438
chegadaY = 27

# imagem do jogador
jogadorImagem = pygame.image.load(os.path.join(diretorio_imagens, 'jogador.png'))
jogadorImagem = pygame.transform.scale(jogadorImagem, (14, 14))
rectJogador = jogadorImagem.get_rect()

# Posiçao do jogador
jogadorX = 25 #438 #25 (Padrão)
jogadorY = 25 #27 #25 (Padrão)
jogadorMudançaX = 0
jogadorMudançaY = 0
# Velocidade do jogador
velocidade = 2
# Contador de vida
vida = 5

# Espessura das paredes limitadoras
espessura = 9

# criando a variavel para armazenar o tempo
tempoMapa1 = 0 
#Tela da logo ---------------------------------------------------------------------------------------
pretoImagem = pygame.image.load(os.path.join(diretorio_imagens, 'preto.png'))
pretoImagem = pygame.transform.scale(pretoImagem, (500,550))
pretoImagem.set_alpha(0)
janela.fill(preto)
logoImagem = pygame.image.load(os.path.join(diretorio_imagens, 'logofinal1.png')).convert()
logoImagem.set_alpha(0)

for i in range(255): #fadein
    pygame.time.delay(20)
    logoImagem.set_alpha(i)
    janela.blit(logoImagem, (0,0))
    pygame.display.flip()

for i in range(255): #fadeout
    pygame.time.delay(3)
    pretoImagem.set_alpha(i)
    janela.blit(pretoImagem, (0,0))
    pygame.display.flip()

informacaoImagem = pygame.image.load(os.path.join(diretorio_imagens, 'whiletrue.png'))
informacaoImagem.set_alpha(0)
for k in range(255): #fadein da segunda imagem
    pygame.time.delay(30)
    informacaoImagem.set_alpha(k)
    janela.blit(informacaoImagem, (0,0))
    pygame.display.flip()
pygame.display.flip()
pygame.time.delay(100)
#Menu do jogo ---------------------------------------------------------------------------------------

def menu (janela,wallpaper):
    pygame.font.init()
    fonte_base      = pygame.font.SysFont("Arial",110)
    strJogador     = ''
    ContadorLetras  = 4
    global nome

    def wallpaper_changer (num_wallpaper):
        fundo = pygame.image.load(os.path.join(diretorio_imagens, 'wallpaper{}.png'.format(num_wallpaper)))
        return fundo

    while janela != 0:
        janela.blit (wallpaper_changer(wallpaper),(0,0))
        pygame.time.delay(200)

        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and wallpaper == 3 and ContadorLetras > 0:
                strJogador = strJogador.upper()
                somClick.play()
                
                if len(strJogador) == 0 and event.key == pygame.K_BACKSPACE:
                    strJogador = ''

                elif event.key == pygame.K_BACKSPACE:
                    strJogador = strJogador[:-1]
                    ContadorLetras += 1

                elif ContadorLetras > 1:
                    strJogador += event.unicode
                    ContadorLetras -= 1
                    strJogador = strJogador.upper()

                elif event.key == pygame.K_SPACE and len(strJogador) == 3:
                    nome = strJogador #Inserindo o nome do jogador na variável nome
                    return strJogador       
        
        text_surface = fonte_base.render(strJogador,True,(255,255,255))
        comando = pygame.key.get_pressed()

        if   wallpaper == 0 and comando[pygame.K_SPACE] : wallpaper = 1; somClick.play()
        elif wallpaper == 1 and comando[pygame.K_UP]    : wallpaper = 3; somClick.play()
        elif wallpaper == 1 and comando[pygame.K_SPACE] : wallpaper = 1; somClick.play()
        elif wallpaper == 1 and comando[pygame.K_DOWN]  : wallpaper = 2; somClick.play()
        elif wallpaper == 2 and comando[pygame.K_SPACE] : wallpaper = 1; somClick.play()
        elif wallpaper == 3                             : janela.blit(text_surface,(160,185))

        pygame.display.update()


menu(janela,0)
#-----------------------------------------------------------------------------------------
janela.fill(preto)  # pinta a cor do fundo
pygame.mixer.music.stop()
musicatema = pygame.mixer.music.load(os.path.join(diretorio_sons, 'Map1Song.mp3'))
pygame.mixer.music.set_volume(0.08)
pygame.mixer.music.play(-1)
# texto 'Nível 1' antes de começar o jogo
NomeNivel1 = pygame.image.load(os.path.join(diretorio_imagens, 'nivel1.png'))
janela.blit(NomeNivel1, (0,0))

pygame.display.flip()
time.sleep(4.5) 
#-----------------------------------------------------------------------------------------------------
listaX = []
listaY = []

janela.fill(azul) # pinta a janela novamente

desenharMapa(mapa1, -5, -5)

for x in range(500): # pega as coordenadas de cada pixel preto do mapa e adiciona em uma lista, para ser possível fazer as colisões.
        for y in range(500):
            if janela.get_at((x, y)) == branco:
                listaX.append(x)
                listaY.append(y)

lista2X = []
lista2Y = []


janela.fill(azul)

janela.blit(mapa2, (-38,16))
for x in range(500):
    for y in range(500):
        if janela.get_at((x,y)) == branco:
            lista2X.append(x)
            lista2Y.append(y)
            

lista3X = []
lista3Y = []

janela.fill(azul)

desenharMapa(mapa3, 16, 16)

for x in range(500):
    for y in range(500):
        if janela.get_at((x,y)) == branco:
            lista3X.append(x)
            lista3Y.append(y)

#------------------------------------------------------------------------------------------------------
sair = False
somtiro.play()
tempoAtual = int(pygame.time.get_ticks()/1000)
while sair != True: #CÓDIGO REFERENTE AO MAPA 1
    tempoMapa1 = int(pygame.time.get_ticks()/1000) - tempoAtual # contagem do tempo
    

    janela.fill(preto) # pinta a janela de preto novamente

    cronometro = fonte.render('Tempo: ' + str(tempoMapa1), True, branco)
    janela.blit(cronometro, (285, 490)) # adiciona o cronometro na tela

    jogador = pygame.Rect(jogadorX, jogadorY, 14, 14)

    chegada = pygame.Rect(chegadaX, chegadaY, 14, 14)

    bala1 = pygame.Rect(bala1X, bala1Y, 10, 10)
    bala2 = pygame.Rect(bala2X, bala2Y, 10, 10)
    bala3 = pygame.Rect(bala3X, bala3Y, 10, 10)

    desenharMapa(mapa1, -5, -5) #desenha o mapa 1
        

    pygame.draw.rect(janela, vermelho, (jogador)) # desenha o jogador
    
    pygame.draw.rect(janela, azul, (chegada)) # desenha a chegada
    
    pygame.draw.rect(janela, rosa, (bala1)) # desenha a bala do canhao 1
    pygame.draw.rect(janela, rosa, (bala2)) # desenha a bala do canhao 2
    pygame.draw.rect(janela, rosa, (bala3)) # desenha a bala do canhao 3
    
    drawBarreirasLimitadoras(branco)
    
    #movimentação das balas
    bala1MudançaX = - velocidadeBala
    bala2MudançaX = - velocidadeBala
    bala3MudançaX = - velocidadeBala

    bala1X += bala1MudançaX
    bala2X += bala2MudançaX
    bala3X += bala3MudançaX

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # evento de fechar o jogo
            sair = True
        if event.type == pygame.KEYDOWN: # evento de controle, movimentar o jogador
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                jogadorMudançaX = - velocidade
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                jogadorMudançaX = velocidade   
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                jogadorMudançaY = - velocidade
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                jogadorMudançaY = velocidade
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                jogadorMudançaX = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                jogadorMudançaY = 0
    
    jogadorX += jogadorMudançaX
    jogadorY += jogadorMudançaY

    
    criarCanhão(canhaoImagem, canhao1X, canhao1Y)
    criarCanhão(canhaoImagem, canhao2X, canhao2Y)
    criarCanhão(canhaoImagem, canhao3X, canhao3Y)

    drawCoracaoHud()

    
    if pygame.Rect(bala1X, bala1Y, 10, 10).collidepoint(0, bala1Y): #se a bala encostar na borda da janela do jogo a variavel auxiliar vai receber o tempo do jogo nesse exato momento
        auxTempoBala1 = tempoMapa1
    if auxTempoBala1 + tempoBala1 == tempoMapa1: # a bala vai ser disparada a cada tempo definido da bala (de 1 a 3) de forma aleatória
        bala1X = canhao1X # a bala volta para a posição inicial
        tempoBala1 = randint(1,3)
        somtiro.play()
    if pygame.Rect(bala2X, bala2Y, 10, 10).collidepoint(0, bala2Y):
        auxTempoBala2 = tempoMapa1
    if auxTempoBala2 + tempoBala2 == tempoMapa1:
        bala2X = canhao2X
        tempoBala2 = randint(1,3)
        somtiro.play()
    if pygame.Rect(bala3X, bala3Y, 10, 10).collidepoint(0, bala3Y):
        auxTempoBala3 = tempoMapa1
    if auxTempoBala3 + tempoBala3 == tempoMapa1:
        bala3X = canhao3X
        tempoBala3 = randint(1,3)
        somtiro.play()
    if jogador.colliderect(bala1) or jogador.colliderect(bala2) or jogador.colliderect(bala3):
        somDano.play()
        time.sleep(1)
        jogadorX = 25
        jogadorY = 25
        vida -= 1
    if vida == 4:
        coracaoImagem5.set_alpha(0)
    elif vida == 3:
        coracaoImagem4.set_alpha(0)
    elif vida == 2:
        coracaoImagem3.set_alpha(0)
    elif vida == 1:
        coracaoImagem2.set_alpha(0)
    if vida == 0:
        somGameOver.play()
        janela.fill(preto)
        pygame.mixer.music.stop()
        janela.blit(gameoverImagem, (0,0))
        pygame.display.flip()
        time.sleep(8)
        sair = True
        
    # Colisão com as paredes
    for i in range(len(listaX)):
        if pygame.Rect(jogadorX, jogadorY, 13, 13).collidepoint(listaX[i], listaY[i]):
            jogadorX -= jogadorMudançaX
            jogadorY -= jogadorMudançaY
        

    # Barreiras limitadoras do jogo
    if jogadorY <= 25:
        jogadorY = 25
    if jogadorY >= 462:
        jogadorY = 462
    if jogadorX <= 25:
        jogadorX = 25
    if jogadorX >= 462:
        jogadorX = 462

    if jogador.colliderect(chegada):
        somChegada.play()
        pontos = tempoMapa1
        
        #-----------------------------------------------------
        # Tela antes do próximo mapa
        janela.fill(preto)

        musicatema = pygame.mixer.music.load(os.path.join(diretorio_sons, 'Map2Song.mp3'))
        pygame.mixer.music.set_volume(0.08)
        pygame.mixer.music.play(-1)

        NomeNivel2 = pygame.image.load(os.path.join(diretorio_imagens, 'nivel2.png'))
        janela.blit(NomeNivel2, (0,0))
        pygame.display.flip()
        time.sleep(6) 
        #-----------------------------------------------------
        jogadorX = 25 #25 (Padrão)
        jogadorY = 60 #29 para pular o mapa 60 (Padrão)

        chegadaX = 25
        chegadaY = 29

        velocidade = 2

        canhaoImagem = pygame.transform.rotate(canhaoImagem, -90)

        canhao1X = 100
        canhao1Y = 475

        canhao2X = 225
        canhao2Y = 475

        canhao3X = 350
        canhao3Y = 475

        canhao4X = 475
        canhao4Y = 25

        bala1X = canhao1X + 8
        bala1Y = canhao1Y
        bala1MudançaX = 0
        bala1MudançaY = 0
        tempoBala1 = randint(1,3)
        auxTempoBala1 = -tempoBala1

        bala2X = canhao2X + 8
        bala2Y = canhao2Y
        bala2MudançaX = 0
        bala2MudançaY = 0
        tempoBala2 = randint(1,3)
        auxTempoBala2 = -tempoBala2

        bala3X = canhao3X + 8
        bala3Y = canhao3Y
        bala3MudançaX = 0
        bala3MudançaY = 0
        tempoBala3 = randint(1,3)
        auxTempoBala3 = -tempoBala3

        bala4X = canhao4X
        bala4Y = canhao4Y + 8
        bala4MudançaX = 0
        bala4MudançaY = 0
        tempoBala4 = 3
        auxTempoBala4 = -tempoBala4

        tempoAtual = int(pygame.time.get_ticks()/1000)
#-------------------------------------------------------------------------------------------------------------------------------------
        while sair != True: #Código do mapa 2
            janela.fill(preto)

            tempoMapa2 = int(pygame.time.get_ticks()/1000) - tempoAtual
            cronometro = fonte.render('Tempo: ' + str(tempoMapa2), True, branco)
            

            janela.blit(cronometro, (285, 490))

            janela.blit(mapa2, (-38, 16))

            jogador = pygame.Rect(jogadorX, jogadorY, 14, 14)

            chegada = pygame.Rect(chegadaX, chegadaY, 14, 14)

            bala1 = pygame.Rect(bala1X, bala1Y, 10, 10)
            bala2 = pygame.Rect(bala2X, bala2Y, 10, 10)
            bala3 = pygame.Rect(bala3X, bala3Y, 10, 10)
            bala4 = pygame.Rect(bala4X, bala4Y, 10, 10)

            pygame.draw.rect(janela, vermelho, (jogador)) # desenha meu jogador

            pygame.draw.rect(janela, azul, (chegada)) # desenha minha chegada
            
            pygame.draw.rect(janela, rosa, (bala1)) # desenha a bala do canhao 1
            pygame.draw.rect(janela, rosa, (bala2)) # desenha a bala do canhao 2
            pygame.draw.rect(janela, rosa, (bala3)) # desenha a bala do canhao 3
            pygame.draw.rect(janela, rosa, (bala4)) # desenha a bala do canhao 4
            
            drawBarreirasLimitadoras(branco)

            bala1Y += bala1MudançaY
            bala2Y += bala2MudançaY
            bala3Y += bala3MudançaY
            bala4X += bala4MudançaX

            bala1MudançaY = - velocidadeBala
            bala2MudançaY = - velocidadeBala
            bala3MudançaY = - velocidadeBala
            bala4MudançaX = - velocidadeBala

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # evento de fechar o jogo
                    sair = True
                if event.type == pygame.KEYDOWN: # evento de controle, movimentar o jogador
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        jogadorMudançaX = - velocidade
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        jogadorMudançaX = velocidade   
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        jogadorMudançaY = - velocidade
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        jogadorMudançaY = velocidade
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                        jogadorMudançaX = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                        jogadorMudançaY = 0
            
            jogadorX += jogadorMudançaX
            jogadorY += jogadorMudançaY


            criarCanhão(canhaoImagem, canhao1X, canhao1Y)
            criarCanhão(canhaoImagem, canhao2X, canhao2Y)
            criarCanhão(canhaoImagem, canhao3X, canhao3Y)
            criarCanhão(canhaoImagem2, canhao4X, canhao4Y)

            drawCoracaoHud()

            # colisao com as paredes
            for i in range(len(lista2X)):
                if pygame.Rect(jogadorX, jogadorY, 13, 13).collidepoint(lista2X[i], lista2Y[i]):
                    jogadorX -= jogadorMudançaX
                    jogadorY -= jogadorMudançaY
                            
            # Barreiras colisão
            if jogadorY <= 25:
                jogadorY = 25
            if jogadorY >= 462:
                jogadorY = 462
            if jogadorX <= 25:
                jogadorX = 25
            if jogadorX >= 462:
                jogadorX = 462

            if pygame.Rect(bala1X, bala1Y, 10, 10).collidepoint(bala1X, 0): #se a bala encostar na borda da janela do jogo a variavel auxiliar vai receber o tempo do jogo nesse exato momento
                auxTempoBala1 = tempoMapa2
            if auxTempoBala1 + tempoBala1 == tempoMapa2: # a bala vai ser disparada a cada tempo definido da bala (de 1 a 3) de forma aleatória
                bala1Y = canhao1Y # a bala volta para a posição inicial
                tempoBala1 = randint(1,3)
                somtiro.play()
            if pygame.Rect(bala2X, bala2Y, 10, 10).collidepoint(bala2X, 0):
                auxTempoBala2 = tempoMapa2
            if auxTempoBala2 + tempoBala2 == tempoMapa2:
                bala2Y = canhao2Y
                tempoBala2 = randint(1,3)
                somtiro.play()
            if pygame.Rect(bala3X, bala3Y, 10, 10).collidepoint(bala3X, 0):
                auxTempoBala3 = tempoMapa2
            if auxTempoBala3 + tempoBala3 == tempoMapa2:
                bala3Y = canhao3Y
                tempoBala3 = randint(1,3)
                somtiro.play()
            if pygame.Rect(bala4X, bala4Y, 10, 10).collidepoint(0, bala4Y):
                auxTempoBala4 = tempoMapa2
            if auxTempoBala4 + tempoBala4 == tempoMapa2:
                bala4X = canhao4X #nao tem variavel tempoBala4 por ser um canhao com um padrão definido de tempo, capaz do jogador prever
                tempoBala4 = randint(3,4)
                somtiro.play()
            if jogador.colliderect(bala1) or jogador.colliderect(bala2) or jogador.colliderect(bala3) or jogador.colliderect(bala4):
                somDano.play()
                time.sleep(1)
                jogadorX = 25
                jogadorY = 60
                vida -= 1
            if vida == 4:
                coracaoImagem5.set_alpha(0)
            elif vida == 3:
                coracaoImagem4.set_alpha(0)
            elif vida == 2:
                coracaoImagem3.set_alpha(0)
            elif vida == 1:
                coracaoImagem2.set_alpha(0)
            if vida == 0:
                somGameOver.play()
                janela.fill(preto)
                pygame.mixer.music.stop()
                janela.blit(gameoverImagem, (0,0))
                pygame.display.flip()
                time.sleep(8)
                sair = True

            if jogador.colliderect(chegada): #passa de mapa
                somChegada.play()
                pontos += tempoMapa2 # tempoMapa1 + tempoMapa2
                #-----------------------------------------------------
                musicatema = pygame.mixer.music.load(os.path.join(diretorio_sons, 'Map3Song.mp3'))
                pygame.mixer.music.set_volume(0.08)
                pygame.mixer.music.play(-1)
                # Tela antes do próximo mapa
                janela.fill(preto)
                NomeNivel3 = pygame.image.load(os.path.join(diretorio_imagens, 'nivel3.png'))
                janela.blit(NomeNivel3, (0,0))
                pygame.display.flip()
                time.sleep(6) 
                #-----------------------------------------------------
                jogadorX = 462 #462
                jogadorY = 25 #25

                chegadaX = 462
                chegadaY = 462

                velocidade = 2

                canhaoImagem = pygame.transform.rotate(canhaoImagem, 90)
                canhaoImagem2 = pygame.transform.rotate(canhaoImagem2, -90)

                canhao1X = 475
                canhao1Y = 100

                canhao2X = 475
                canhao2Y = 225

                canhao3X = 475
                canhao3Y = 350

                canhao4X = 2
                canhao4Y = 162

                canhao5X = 2
                canhao5Y = 280

                canhao6X = 225
                canhao6Y = 475

                bala1X = canhao1X
                bala1Y = canhao1Y + 8
                bala1MudançaX = 0
                bala1MudançaY = 0
                tempoBala1 = randint(1,2)
                auxTempoBala1 = -tempoBala1

                bala2X = canhao2X
                bala2Y = canhao2Y + 8
                bala2MudançaX = 0
                bala2MudançaY = 0
                tempoBala2 = randint(1,2)
                auxTempoBala2 = -tempoBala2

                bala3X = canhao3X
                bala3Y = canhao3Y
                bala3MudançaX = 0
                bala3MudançaY = 0
                tempoBala3 = randint(1,2)
                auxTempoBala3 = -tempoBala3

                bala4X = canhao4X + 12
                bala4Y = canhao4Y + 8
                bala4MudançaX = 0
                bala4MudançaY = 0
                tempoBala4 = 3
                auxTempoBala4 = -tempoBala4

                bala5X = canhao5X
                bala5Y = canhao5Y + 8
                bala5MudançaX = 0
                bala5MudançaY = 0
                tempoBala5 = randint(1,2)
                auxTempoBala5 = -tempoBala5

                bala6X = canhao6X + 8
                bala6Y = canhao6Y
                bala6MudançaX = 0
                bala6MudançaY = 0
                tempoBala6 = randint(1,2)
                auxTempoBala6 = -tempoBala6

                somtiro.play()

                mudouChegada = False

                tempoAtual = int(pygame.time.get_ticks()/1000)
                while sair != True: #Código do mapa 3
                    janela.fill(preto)

                    tempoMapa3 = int(pygame.time.get_ticks()/1000) - (tempoAtual)
                    cronometro = fonte.render('Tempo: ' + str(tempoMapa3), True, branco)

                    janela.blit(cronometro, (285, 490))

                    desenharMapa(mapa3, 16, 16)
                    

                    jogador = pygame.Rect(jogadorX, jogadorY, 12, 12)

                    chegada = pygame.Rect(chegadaX, chegadaY, 12, 12)


                    pygame.draw.rect(janela, vermelho, (jogador)) # desenha meu jogador

                    pygame.draw.rect(janela, azul, (chegada)) # desenha minha chegada

                    bala1 = pygame.Rect(bala1X, bala1Y, 10, 10)
                    bala2 = pygame.Rect(bala2X, bala2Y, 10, 10)
                    bala3 = pygame.Rect(bala3X, bala3Y, 10, 10)
                    bala4 = pygame.Rect(bala4X, bala4Y, 10, 10)
                    bala5 = pygame.Rect(bala5X, bala5Y, 10, 10)
                    bala6 = pygame.Rect(bala6X, bala6Y, 10, 10)

                    pygame.draw.rect(janela, rosa, (bala1)) # desenha a bala do canhao 1
                    pygame.draw.rect(janela, rosa, (bala2)) # desenha a bala do canhao 2
                    pygame.draw.rect(janela, rosa, (bala3)) # desenha a bala do canhao 3
                    pygame.draw.rect(janela, rosa, (bala4)) # desenha a bala do canhao 4
                    pygame.draw.rect(janela, rosa, (bala5)) # desenha a bala do canhao 5
                    pygame.draw.rect(janela, rosa, (bala6)) # desenha a bala do canhao 6


                    drawBarreirasLimitadoras(branco)

                    bala1X += bala1MudançaX
                    bala2X += bala2MudançaX
                    bala3X += bala3MudançaX
                    bala4X += bala4MudançaX
                    bala5X += bala5MudançaX
                    bala6Y += bala6MudançaY

                    bala1MudançaX = - velocidadeBala
                    bala2MudançaX = - velocidadeBala
                    bala3MudançaX = - velocidadeBala
                    bala4MudançaX = velocidadeBala
                    bala5MudançaX = velocidadeBala
                    bala6MudançaY = - velocidadeBala

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: # evento de fechar o jogo
                            sair = True
                        if event.type == pygame.KEYDOWN: # evento de controle, movimentar o jogador
                            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                jogadorMudançaX = - velocidade
                            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                jogadorMudançaX = velocidade   
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                jogadorMudançaY = - velocidade
                            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                jogadorMudançaY = velocidade
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                                jogadorMudançaX = 0
                            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                                jogadorMudançaY = 0
                    
                    jogadorX += jogadorMudançaX
                    jogadorY += jogadorMudançaY

                    criarCanhão(canhaoImagem, canhao1X, canhao1Y)
                    criarCanhão(canhaoImagem, canhao2X, canhao2Y)
                    criarCanhão(canhaoImagem, canhao3X, canhao3Y)
                    criarCanhão(canhaoImagem3, canhao4X, canhao4Y)
                    criarCanhão(canhaoImagem3, canhao5X, canhao5Y)
                    criarCanhão(canhaoImagem2, canhao6X, canhao6Y)

                    drawCoracaoHud()

                    # colisao com as paredes
                    for i in range(len(lista3X)):
                        if pygame.Rect(jogadorX, jogadorY, 11, 11).collidepoint(lista3X[i], lista3Y[i]):
                            jogadorX -= jogadorMudançaX
                            jogadorY -= jogadorMudançaY


                     
                    if jogadorY <= 25:
                        jogadorY = 25
                    if jogadorY >= 462:
                        jogadorY = 462
                    if jogadorX <= 25:
                        jogadorX = 25
                    if jogadorX >= 462:
                        jogadorX = 462

                    if pygame.Rect(bala1X, bala1Y, 10, 10).collidepoint(0, bala1Y): #se a bala encostar na borda da janela do jogo a variavel auxiliar vai receber o tempo do jogo nesse exato momento
                        auxTempoBala1 = tempoMapa3
                    if auxTempoBala1 + tempoBala1 == tempoMapa3: # a bala vai ser disparada a cada tempo definido da bala (de 1 a 3) de forma aleatória
                        bala1X = canhao1X # a bala volta para a posição inicial
                        tempoBala1 = randint(1,3)
                        somtiro.play()
                    if pygame.Rect(bala2X, bala2Y, 10, 10).collidepoint(0, bala2Y):
                        auxTempoBala2 = tempoMapa3
                    if auxTempoBala2 + tempoBala2 == tempoMapa3:
                        bala2X = canhao2X
                        tempoBala2 = randint(1,3)
                        somtiro.play()
                    if pygame.Rect(bala3X, bala3Y, 10, 10).collidepoint(0, bala3Y):
                        auxTempoBala3 = tempoMapa3
                    if auxTempoBala3 + tempoBala3 == tempoMapa3:
                        bala3X = canhao3X
                        tempoBala3 = randint(1,3)
                        somtiro.play()
                    if pygame.Rect(bala4X, bala4Y, 10, 10).collidepoint(500, bala4Y):
                        auxTempoBala4 = tempoMapa3
                    if auxTempoBala4 + tempoBala4 == tempoMapa3:
                        bala4X = canhao4X + 8
                        tempoBala4 = randint(1,3)
                        somtiro.play()
                    if pygame.Rect(bala5X, bala5Y, 10, 10).collidepoint(500, bala5Y):
                        auxTempoBala5 = tempoMapa3
                    if auxTempoBala5 + tempoBala5 == tempoMapa3:
                        bala5X = canhao5X + 8
                        tempoBala5 = randint(1,3)
                        somtiro.play()
                    if pygame.Rect(bala6X, bala6Y, 10, 10).collidepoint(bala6X, 0):
                        auxTempoBala6 = tempoMapa3
                    if auxTempoBala6 + tempoBala6 == tempoMapa3:
                        bala6Y = canhao6Y
                        tempoBala6 = randint(1,3)
                        somtiro.play()
                    if jogador.colliderect(bala1) or jogador.colliderect(bala2) or jogador.colliderect(bala3) or jogador.colliderect(bala4) or jogador.colliderect(bala5) or jogador.colliderect(bala6):
                        somDano.play()
                        time.sleep(1)
                        jogadorX = 462
                        jogadorY = 25
                        vida -= 1
                        if mudouChegada == True:
                            jogadorX = 462
                            jogadorY = 462

                    if vida == 4:
                        coracaoImagem5.set_alpha(0)
                    elif vida == 3:
                        coracaoImagem4.set_alpha(0)
                    elif vida == 2:
                        coracaoImagem3.set_alpha(0)
                    elif vida == 1:
                        coracaoImagem2.set_alpha(0)
                    if vida == 0:
                        somGameOver.play()
                        janela.fill(preto)
                        pygame.mixer.music.stop()
                        janela.blit(gameoverImagem, (0,0))
                        pygame.display.flip()
                        time.sleep(8)
                        sair = True

                    if jogador.colliderect(chegada):
                        somChegada.play()
                        chegadaX = 25
                        chegadaY = 25
                        mudouChegada = True 
                        
                    if chegadaX == 25 and chegadaY == 25 and jogador.colliderect(pygame.Rect(25,25, 12,12)):
                        pontos = tempoMapa1 + tempoMapa2 + tempoMapa3

                        #Inserindo pontuação e nome no banco de dados:
                        cursor.execute("INSERT INTO nomes_pontos VALUES("+str(pontos)+",'"+nome+"')")
                        
                        #Ordenando os registros de acordo com a pontuação de maneira crescente
                        cursor.execute("SELECT rowid, * FROM nomes_pontos ORDER BY Score LIMIT 10")
                        
                        itens1 = cursor.fetchmany(10) #Atualizando o valor de itens1 após o fim do jogo
                        banco_de_dados.commit() #Aplicando alterações no banco de dados.
                        banco_de_dados.close() #Fechando conexão com o banco de dados
                        tela_rank(largura_janela,altura_janela)

                    pygame.display.flip() 
                    clock.tick(60)
                
            pygame.display.flip()  
            clock.tick(60)

    pygame.display.flip() # atualiza a tela 
    clock.tick(60)
