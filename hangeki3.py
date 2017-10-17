# -*- coding: cp1252 -*-
# Faz as importações necessarias
#import tela_inicial
import pygame, math, os
from random import randrange
from pygame.locals import *
## importa o arquivo que contem as funções basicas
import Funcoes

# Define a tela para ser iniciada sempre no centro
os.environ['SDL_VIDEO_CENTERED'] = '1'
#Inicia pygame
pygame.init()
#Inicia a font do pygame
pygame.font.init()

# Classe que representa a tela
class Tela():
    def __init__(self):
        self.nomeTela = 'Hangeki'
        self.altura = Funcoes.alt_disp
        self.largura = Funcoes.larg_disp
        #self.background = 'resources\\background1.jpg'

#Classe responsavel por gerenciar o jogo
class Game():
    def __init__(self):
        '''
        1 = ativo
        2 = pausado
        3 = gameOver
        '''
        self.status = 1
        self.score = 0
        self.font_name = 'NasalizationRg-Regular'#pygame.font.get_default_font()
        self.game_font = pygame.font.SysFont(self.font_name, 20)
        self.Avioes = 3
        self.fase = 1
        self.asteroids = 5
        self.modo = 1
        self.bossWave = 5

    def atualizaScore(self,ponto):
        self.score += ponto

# Classe da nave
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Carregando imagens das animações pois o blit ferra
        self.angulo = 0
        self.x = tela.largura/2
        self.y = tela.altura/2
        self.speed = 0
        self.vidas = 10
        self.rect = pygame.Rect(self.x, self.y, self.largura-10, self.altura-10)
        self.rady = 0
        self.radx = 0
        self.anim = 0
        self.countAnim = 0
        self.tiraVida = False
        self.image = pygame.image.load("resources\\Nave_0.png").convert_alpha()
   
    #metodo que ira atualizar a posição da nave, rotaciona-la e anima-la
    def atualiza(self):
        self.rect = pygame.Rect(self.x, self.y, self.largura-10, self.altura-10)
        if(self.anim > 3):
            self.anim = 0
            
    def viraEsquerda(self):
        if self.angulo < 150:
            self.angulo += 5
    
    def viraDireita(self):
        if self.angulo > 30:
            self.angulo -= 5
    def shoot(self):
        tiros.append(Tiro(int(self.x), int(self.y), self.angulo))

#Classe responsavel por gerenciar os tiros da nave      
class Tiro(pygame.sprite.Sprite):
    def __init__(self,x,y,angulo):
        self.altura = 31
        self.largura = 5
        self.angulo = angulo
        self.speed = 15
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x+34, self.y+37, self.largura, self.altura)
        
    def atualiza(self):     
        self.rect = pygame.Rect(self.x+34, self.y+37, self.largura, self.altura)   
            
    def disparo(self):
        real_angulo=self.angulo+90
        real_angulo*=math.pi/180
        rady=-math.sin(real_angulo)
        radx=math.cos(real_angulo)

        if (rady<0):
            self.y+=rady*self.speed
        if (rady>0):
            self.y+=+rady*self.speed
        if (radx<0):
            self.x+=radx*self.speed
        if (radx>0):
            self.x+=+radx*self.speed

#Caso os tiros saiam da tela eles são deletados para n consumir tanta memoria                        
def removeTiros(tiros):
    for tiro in range(len(tiros)):
        if(tiros[tiro].y > tela.altura+tiros[tiro].altura
            or tiros[tiro].y < 0 - tiros[tiro].altura
            or tiros[tiro].x > tela.largura
            or tiros[tiro].x < -74):
                del tiros[tiro]
                break
            
#Função main do jogo
def main(altura,largura,controle):
    '''
    
    Declaração de variaveis
    criação da tela com a largura e altura baseadas no txt com os parametros
    as variaveis globais são utilizadas em outros metodos
    declara os arrays de tiros e de asteroids
    estancia o Boss
    declara os ticks para a criação de asteroids e dos tiros
    carrega a imagem de background
    define o clock para fazer o controle de fps do jogo
    cria variaves para o controle
    '''
    gravaScore = False
    BLACK = (0,0,0)
    global tela
    tela = Tela()
    tela.largura = largura
    tela.altura = altura
    global screen
    screen = pygame.display.set_mode((tela.largura,tela.altura),0,32)
    pygame.display.set_caption(tela.nomeTela)
    background = BLACK
    global nave
    nave = Nave()
    global game
    game = Game()
    game.controle = controle
    tamTiros = 0
    tick_shoot = 0
    estFase = False
    contAsteroids = 0
    tamTiros = 0
    clock = pygame.time.Clock()

    # se o status do jogo for ativo ou pausado
    while game.status in(1,2):
        #define FPS para ser 60
        clock.tick(60)
        pause = False
        if not estFase:
            if game.modo == 1:
                if tick_asteroid <= 0:
                    tick_asteroid = 35
                    #asteroids.append(Asteroid())
                    #contAsteroids += 1
                else:
                    if tick_asteroid > 0:
                        tick_asteroid -= 1
        for event in pygame.event.get():
            #se clicar em fechar ele troca o status e fecha o jogo
            if event.type == pygame.QUIT:
                screen.blit(background,(0,0))
                game.status = 4        
        tecla_pressionada = pygame.key.get_pressed()
        # caso aperte P pausa o jogo
        if tecla_pressionada[K_p]:
            game.status = 2
        #caso aperte espaço ou aperte o botao 3 cria um tiro 
        if tecla_pressionada[K_SPACE] or button3 == 1:
            if tick_shoot <= 0:
                tick_shoot = 15
                nave.shoot()
            else:
                if tick_shoot > 0:
                    tick_shoot -= 1
        # o mesmo para as rotações
        if tecla_pressionada[K_LEFT] and game.modo == 1:
            nave.viraEsquerda()
        if tecla_pressionada[K_RIGHT] and game.modo == 1:
            nave.viraDireita()

        #if game.controle == 2:
            #pega o status do click e verifica se ele está colidindo com as imagens dos controles
        #pause
        #desenha o background
        screen.blit(background,(0,0))
        
        #desenha os tiros
        tamTiros = len(tiros)
        if tamTiros-1 >= 0:
            for i in range(tamTiros):
                tiros[i].atualiza()
                tiros[i].disparo()
                screen.blit(tiros[i].image, (tiros[i].x, tiros[i].y))
        #atualiza a posição da nave e a desenha
        nave.atualiza()
        screen.blit(nave.image, (nave.x, nave.y))
        #verifica se necessario deletar os tiros do bos e da nave
        removeTiros(tiros)
if __name__ == "__main__":
    #lê arquivo e atribui os valores nas variaveis
    Funcoes.lerArquivo()
    main(600,800,Funcoes.controle)
    

