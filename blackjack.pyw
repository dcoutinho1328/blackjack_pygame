import pygame as pg
import random

sair = True
naipes = {'Paus', 'Espadas', 'Copas', 'Ouros'}
tipos = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
numeros = (2,3,4,5,6,7,8,9,10,10,10,10,11)
valores = dict(zip(tipos,numeros))

pg.init()

BG = pg.Color(60,179,113)
BLACK = pg.Color(28,28,28)
WHITE = pg.Color(255,250,250)
RED = pg.Color(255,0,0)
PLACAR = pg.Color(176,224,230)
CLIQUE = pg.Color(255,255,224)
altura = 500
largura = 800
x_carta = 70
frente = pg.image.load('Frente.png')
tras = pg.image.load('Tras.png')
paus = pg.image.load('Paus.png')
copas = pg.image.load('Copas.png')
ouros = pg.image.load('Ouros.png')
espadas = pg.image.load('Espadas.png')
icon = pg.image.load('icone.ico')
fonte = pg.font.Font('arial.ttf', 40)
fonte_fichas = pg.font.Font('arial.ttf', 16)
fonte_cmd = pg.font.Font('arial.ttf', 25)
placar = pg.Rect(0,470,800,30)
clique_comprar = pg.Rect(15,170,90,130)
clique_segurar = pg.Rect(195,225,100,30)
clique_sim = pg.Rect(345,195,80,50)
clique_nao = pg.Rect(345,295,80,50)
clique_prox = pg.Rect(645,223,105,30)
img_naipes = {'Paus':paus, 'Espadas':espadas, 'Copas':copas, 'Ouros':ouros}
x_s = (28,28,28,28,28,28,28,28,16,28,23,25,25)
dx = dict(zip(tipos,x_s))

class Carta:

    def __init__ (self, naipe, tipo):
        self.naipe = naipe
        self.tipo = tipo

    def __str__(self):
        return '{} de {}'.format(self.tipo, self.naipe)

class Baralho:

    def __init__ (self):
        self.baralho = []
        for naipe in naipes:
            for tipo in tipos:
                self.baralho.append(Carta(naipe, tipo))

    def __str__(self):
        conteudo = 'Cartas no baralho:'
        for carta in self.baralho:
            conteudo = conteudo + '\n' + str(carta)
        return conteudo

    def __len__(self):
        return len(self.baralho)

    def embaralhar(self):
        random.shuffle(self.baralho)

    def deal(self):
        return self.baralho.pop(0)

class Mao:
    
    def __init__ (self):
        self.cartas = []
        self.valor = 0
        self.azes = 0

    def adc_carta(self, carta):
        self.cartas.append(carta)
        self.valor += valores[carta.tipo]
        if carta.tipo == 'A':
            self.azes += 1
        
    def ajuste_para_as(self):
        while self.valor > 21 and self.azes != 0:
            self.valor -= 10
            self.azes -= 1

class Fichas:

    def __init__(self):
        self.total = 500
        self.aposta = 50

    def vencer_aposta(self):
        self.total += self.aposta

    def perder_aposta (self):
        self.total -= self.aposta

def comprar(baralho, mao):
    carta = baralho.deal()
    mao.adc_carta(carta)
    mao.ajuste_para_as()

def mostrar_algumas(jogador, dealer, janela):
    janela.blit(tras, (40,10))
    janela.blit(tras, (130,10))
    i=0
    for i in range(len(jogador.cartas)):
        carta = jogador.cartas[i]
        x = 40+i*90
        y=340
        if carta.naipe == 'Paus' or carta.naipe == 'Espadas':
            cor = BLACK
        else:
            cor = RED
        janela.blit(frente,(x,y))
        janela.blit(img_naipes[carta.naipe],(x+20,y+70))
        janela.blit(fonte.render(carta.tipo, True, cor), (x+dx[carta.tipo],y+10))

def mostrar_todas(jogador, dealer, janela):
    i=0
    for i in range(len(dealer.cartas)):
        carta = dealer.cartas[i]
        x = 40+i*90
        y=10
        if carta.naipe == 'Paus' or carta.naipe == 'Espadas':
            cor = BLACK
        else:
            cor = RED
        janela.blit(frente,(x,y))
        janela.blit(img_naipes[carta.naipe],(x+20,y+70))
        janela.blit(fonte.render(carta.tipo, True, cor), (x+dx[carta.tipo],y+10))
    

def jogador_estoura(fichas, janela):
    janela.blit(fonte_cmd.render('Você Estourou!', True, RED), (400, 225))
    fichas.perder_aposta()

def jogador_vence(fichas, janela):
    janela.blit(fonte_cmd.render('Você Venceu!', True, BLACK), (400, 225))
    fichas.vencer_aposta()
    #verificar

def dealer_estoura(fichas, janela):
    janela.blit(fonte_cmd.render('O Dealer Estourou!', True, BLACK), (400, 225))
    fichas.vencer_aposta()
    #verificar

def dealer_vence(fichas, janela):
    janela.blit(fonte_cmd.render('O Dealer Venceu!', True, RED), (400, 225))
    fichas.perder_aposta()

def empate(janela):
    janela.blit(fonte_cmd.render('Empate', True, BLACK), (400, 225))

jan = pg.display.set_mode([largura, altura])
pg.display.set_caption('Blackjack')
pg.display.set_icon(icon)
baralho = Baralho()
jogador = Mao()
dealer = Mao()
fichas = Fichas()
baralho.embaralhar()
comprar(baralho, dealer)
comprar(baralho, dealer)
comprar(baralho, jogador)
comprar(baralho, jogador)
playing = True
jan.fill(BG)



while sair:
    if fichas.total>0:
        jan.fill(PLACAR, rect=placar)
        jan.blit(tras, (20, 175))
        if fichas.total == 1:
            jan.blit(fonte_fichas.render('Fichas: 0'.format(fichas.total), True, BLACK), (20, 477))
        else:    
            jan.blit(fonte_fichas.render('Fichas: {}'.format(fichas.total), True, BLACK), (20, 477))
            jan.blit(fonte_fichas.render('Aposta: 50', True, BLACK), (700, 477))
        jan.blit(fonte_fichas.render('Jogador: {}'.format(jogador.valor), True, BLACK), (300, 477))
        if playing:
            jan.blit(fonte_fichas.render('Dealer: ???', True, BLACK), (400, 477))
        else:
            jan.blit(fonte_fichas.render('Dealer: {}'.format(dealer.valor), True, BLACK), (400, 477))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sair = False
            elif playing:
                jan.blit(fonte_cmd.render('Segurar', True, BLACK), (200, 225))
                mostrar_algumas(jogador,dealer,jan)
                if event.type == pg.MOUSEMOTION:
                    if (event.pos[0] > 20 and event.pos[0] < 100) and (event.pos[1] > 175 and event.pos[1] < 295):
                        jan.fill(PLACAR, rect=clique_comprar)
                        jan.blit(tras, (20, 175))
                    else:
                        jan.fill(BG, rect=clique_comprar)
                        jan.blit(tras, (20, 175))
                    if (event.pos[0] > 195 and event.pos[0] < 295) and (event.pos[1] > 225 and event.pos[1] < 255):
                        jan.fill(PLACAR, rect=clique_segurar)
                        jan.blit(fonte_cmd.render('Segurar', True, BLACK), (200, 225))
                    else:
                        jan.fill(BG, rect=clique_segurar)
                        jan.blit(fonte_cmd.render('Segurar', True, BLACK), (200, 225))
                if event.type == pg.MOUSEBUTTONDOWN:
                    if (event.pos[0] > 20 and event.pos[0] < 100) and (event.pos[1] > 175 and event.pos[1] < 295) and event.button==1:
                        jan.fill(CLIQUE, rect=clique_comprar)
                        jan.blit(tras, (20, 175))
                        comprar(baralho,jogador)
                        mostrar_algumas(jogador,dealer,jan)
                        if jogador.valor >=21:
                            if jogador.valor > 21:
                                jogador_estoura(fichas, jan)
                                if fichas.total == 0:
                                    fichas.total = 1
                            playing=False
                            flg = 3
                            jan.blit(fonte_fichas.render('Valor da mão: {}'.format(jogador.valor), True, BLACK), (400, 477))
                    else:
                        jan.fill(BG, rect=clique_comprar)
                        jan.blit(tras, (20, 175))
                    if (event.pos[0] > 195 and event.pos[0] < 295) and (event.pos[1] > 225 and event.pos[1] < 255) and event.button==1:
                        jan.fill(CLIQUE, rect=clique_segurar)
                        jan.blit(fonte_cmd.render('Segurar', True, BLACK), (200, 225))
                        playing=False
                        flg=3
                    else:
                        jan.fill(BG, rect=clique_segurar)
                        jan.blit(fonte_cmd.render('Segurar', True, BLACK), (200, 225))
                if event.type == pg.MOUSEBUTTONUP:
                    if (event.pos[0] > 20 and event.pos[0] < 100) and (event.pos[1] > 175 and event.pos[1] < 295):
                        jan.fill(PLACAR, rect=clique_comprar)
                        jan.blit(tras, (20, 175))

            else:
                if flg == 3:
                    if jogador.valor <= 21:
                        while True: 
                            if dealer.valor > jogador.valor:
                                dealer_vence(fichas,jan)
                                if fichas.total == 0:
                                    fichas.total=1
                                flg = 22
                                break
                            elif dealer.valor < jogador.valor:
                                comprar(baralho, dealer)
                                if dealer.valor > 21:
                                    dealer_estoura(fichas,jan)
                                    flg = 22
                                    break
                                else:
                                    continue
                            elif dealer.valor == jogador.valor and jogador.valor < 16:
                                comprar(baralho, dealer)
                                if dealer.valor > 21:
                                    dealer_estoura(fichas,jan)
                                    flg = 22
                                    break
                                else:
                                    continue
                            else:
                                empate(jan)
                                flg =22
                                break
                mostrar_todas(jogador, dealer, jan)
                jan.fill(BG, rect=clique_segurar)
                jan.blit(fonte_cmd.render('Segurar', True, BLACK), (200, 225))
                jan.fill(BG, rect=clique_comprar)
                jan.blit(tras, (20, 175))
                jan.blit(fonte_cmd.render('Próxima', True, BLACK), (650, 225))
                if event.type == pg.MOUSEMOTION:
                    if (event.pos[0]>645 and event.pos[0]<785) and (event.pos[1]>220 and event.pos[1]<250):
                        jan.fill(PLACAR, rect=clique_prox)
                        jan.blit(fonte_cmd.render('Próxima', True, BLACK), (650, 225))
                    else:
                        jan.fill(BG, rect=clique_prox)
                        jan.blit(fonte_cmd.render('Próxima', True, BLACK), (650, 225))
                if event.type == pg.MOUSEBUTTONDOWN:
                    if (event.pos[0]>645 and event.pos[0]<785) and (event.pos[1]>220 and event.pos[1]<250) and event.button==1:
                        jan.fill(PLACAR, rect=clique_prox)
                        jan.blit(fonte_cmd.render('Próxima', True, BLACK), (650, 225))
                        baralho = Baralho()
                        jogador = Mao()
                        dealer = Mao()
                        baralho.embaralhar()
                        comprar(baralho, dealer)
                        comprar(baralho, dealer)
                        comprar(baralho, jogador)
                        comprar(baralho, jogador)
                        playing = True
                        jan.fill(BG)
                        if fichas.total==1:
                            fichas.total=0

                
            
    else:
        jan.blit(fonte.render('Deseja jogar novamente?', True, BLACK), (170, 100))
        jan.blit(fonte.render('Sim', True, WHITE), (350, 200))
        jan.blit(fonte.render('Não', True, WHITE), (350, 300))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sair = False
            if event.type == pg.MOUSEMOTION:
                if (event.pos[0]>345 and event.pos[0]<425) and (event.pos[1]>195 and event.pos[1]<245):
                    jan.fill(PLACAR, rect=clique_sim)
                    jan.blit(fonte.render('Sim', True, WHITE), (350, 200))

                elif (event.pos[0]>345 and event.pos[0]<425) and (event.pos[1]>295 and event.pos[1]<345):
                    jan.fill(PLACAR, rect=clique_nao)
                    jan.blit(fonte.render('Não', True, WHITE), (350, 300))
                    
                else:
                    jan.fill(BG, rect=clique_sim)
                    jan.blit(fonte.render('Sim', True, WHITE), (350, 200))
                    jan.fill(BG, rect=clique_nao)
                    jan.blit(fonte.render('Não', True, WHITE), (350, 300))
                    
            if event.type == pg.MOUSEBUTTONDOWN:
                if (event.pos[0]>345 and event.pos[0]<425) and (event.pos[1]>195 and event.pos[1]<245) and event.button==1:
                    jan.fill(CLIQUE, rect=clique_sim)
                    jan.blit(fonte.render('Sim', True, WHITE), (350, 200))
                    baralho = Baralho()
                    jogador = Mao()
                    dealer = Mao()
                    fichas = Fichas()
                    baralho.embaralhar()
                    comprar(baralho, dealer)
                    comprar(baralho, dealer)
                    comprar(baralho, jogador)
                    comprar(baralho, jogador)
                    playing = True
                    jan.fill(BG)
                    
                elif (event.pos[0]>345 and event.pos[0]<425) and (event.pos[1]>295 and event.pos[1]<345) and event.button==1:
                    jan.fill(CLIQUE, rect=clique_nao)
                    jan.blit(fonte.render('Não', True, WHITE), (350, 300))
                    sair = False
                    
                 
    pg.display.update()
    
pg.quit()
    
