from PPlay.window import *
from PPlay.gameimage import *
from PPlay.mouse import Mouse
from PPlay.sprite import *
from PPlay.collision import *
from PPlay.mouse import Mouse
from menu_projetofinal import Menu
from ranking import Ranking
import variables
import random
import pygame

janela = Window(1000, 600)
janela.set_title("Life on the River") # Usando parênteses para chamar a função
fundojogo1 = Sprite("fundo_jogo.png") 
fundojogo1.x = 0
fundojogo1.y = 0
imagem_invertida = pygame.transform.flip(fundojogo1.image, True, False)

fundojogo2 = Sprite("fundo_jogo.png") # Carregamos a imagem original novamente só para criar o objeto
fundojogo2.image = imagem_invertida   # AGORA substituímos pela imagem invertida
fundojogo2.x = fundojogo1.width      # Posiciona ao lado da primeira
fundojogo2.y = 0

teclado = janela.get_keyboard()
player = Sprite("burglar.png", 9)
playerabaixado = Sprite("burglar_state2.png")
helicopter = Sprite("helicoptero.png",3)
helicopter.x = 6000
helicopter.y = 100
helicopter.set_total_duration(300)
helicopter.set_sequence(0,2)
player.x = 400
player.y = janela.height - player.height
playerabaixado.x = 400
playerabaixado.y = 525
player.set_total_duration(900)
player.set_sequence(0,4)
money_bag = Sprite("saco_de_dinheiro.png")
money_bag.x = 1000
money_bag.y = janela.height - money_bag.height
bullet = Sprite("bala_projetofinal.png")
bullet.x = 0 - bullet.width
bullet.y = 500
car_item = Sprite("carro.png")
car = Sprite("carroinvertido.png")
car.x = 400
car.y = 495
car_item.x = 1000
car_item.y = 560
helicopter_bullet=Sprite("helicopter_bullet.png")
helicopter_bullet.x = 700
helicopter_bullet.y = 340
immunity = False
cont = 0
pontos = 0
pulo = False
pulomaximo = False
abaixado = False
gameover = False
spawnaritem = False
tiro_helicoptero = False
cronometropulo = 1.2
cronometroabaixado = 0
cronometroimmu = 0
vel = 25
massa = 1
bonus = 1
items = 0
cronometroresetitem = 0
spawnaritens = 0
sorteio = 300
cronometrobonus = 0
police_car = Sprite("viatura.png")
police_car.x = 1000
police_car.y = 515
sorteioinimigos = 100
inimigos = 0
velheli = 100
mouse = Mouse()
menu = Menu(janela) # Crie o menu uma vez, fora do loop

while True:
    if variables.game_state == 1:
        janela.set_title("Life on the River - Menu")
        menu.run() # Executa a lógica do menu
    elif variables.game_state == 2:
        janela.set_background_color([0,0,0])
        fundojogo1.draw()
        fundojogo2.draw()
        if fundojogo1.x <= -1000:
            fundojogo1.x = 1000
        if fundojogo2.x <= -1000:
            fundojogo2.x = 1000
        if pulo == False and pulomaximo == False and immunity == False :
            if teclado.key_pressed("UP"):
                if cronometropulo > 1 :
                    pulo = True
                    cronometropulo = 0
                    player.set_sequence(5,6)

        if teclado.key_pressed("DOWN") and pulo == False and pulomaximo == False and immunity == False:
            abaixado = True
            cronometroabaixado = 0
        if abaixado == True and cronometroabaixado > 0.5:
            cronometroabaixado = 0
            abaixado = False
        if teclado.key_pressed("ESC"):
            variables.game_state = 1
            cont = 0
            pontos = 0
            pulo = False
            pulomaximo = False
            abaixado = False
            gameover = False
            cronometropulo = 1.2
            cronometroabaixado = 0
            abaixado = False
            pulo = False
            pulomaximo = False
            player.set_sequence(0,4)
            player.y = janela.height - player.height
        if pulo == True:
            if player.y > 200:
               player.y -= (1/2) * massa * (vel**2)*janela.delta_time()
            else:
                pulomaximo = True
                pulo = False
        if pulomaximo == True:
            if player.y < 470:
                 player.y += (1/2) * massa * (vel**2)*janela.delta_time()
                 player.set_sequence(7,8)
            else:
                pulomaximo = False
                player.set_sequence(0,4)
        
        cronometropulo += janela.delta_time()
        cont += 1
        cronometroabaixado += janela.delta_time()
        if cont % 10 == 0:
            pontos  += 1 * bonus
        if abaixado == False and immunity == False:
            player.draw()
            player.update()
        elif abaixado == True and immunity == False:
            playerabaixado.draw()
        if pontos % sorteio == 0 and pontos > 0 and items == 0:
           items = random.randint(1,2)
           sorteio = random.randint(400,1000)
           
        if pontos % sorteioinimigos == 0 and inimigos == 0 and pontos > 0 and tiro_helicoptero == False:
            inimigos = random.randint(1,2)
            sorteioinimigos = random.randint(100,200)
           
        if items  == 1:
            money_bag.x -= 200 * janela.delta_time()*variables.dificuldade
        if (Collision.collided(player, money_bag)) or (Collision.collided(playerabaixado, money_bag)) and abaixado == True or (Collision.collided(car, money_bag)) and immunity == True :
            bonus = 2

        if bonus == 2:
            cronometrobonus += janela.delta_time()
        if cronometrobonus >= 10:
            bonus = 1
            cronometrobonus = 0
        if money_bag.x <= 0 - money_bag.width or  (Collision.collided(playerabaixado, money_bag)) and abaixado == True  or Collision.collided(player, money_bag):
            items = 0
            money_bag.x = 1000
            
            
        if items == 2:
            car_item.x -= 200*janela.delta_time()*variables.dificuldade
        if car_item.x <= 0 - car_item.width:
            items = 0
            car_item.x = 1000
        if (Collision.collided(player, car_item)) and car_item.x <= 435  or (Collision.collided(playerabaixado, car_item)) and abaixado == True  :
            items = 0
            car_item.x = 1000
            
            immunity = True
        if immunity == True:   
            car.draw()
            cronometroimmu+=janela.delta_time()
            janela.draw_text(str(int(cronometroimmu)),200, 0, size=30, color=(255,0,0), font_name="pricedown bl", bold=False, italic=False)
            if cronometroimmu >= 10:
                cronometroimmu = 0
                immunity = False
        if inimigos == 1:
            bullet.x += 200*janela.delta_time()*variables.dificuldade
        if bullet.x >=1000:
            bullet.x = 0 - bullet.width
            inimigos = 0
        if inimigos == 2:
            police_car.x -= 200*janela.delta_time()*variables.dificuldade
        if police_car.x <=0 - police_car.width:
            police_car.x = 1000
            inimigos = 0
        helicopter.x = helicopter.x + velheli*janela.delta_time()*variables.dificuldade
        if helicopter.x <=700:
            tiro_helicoptero = True
            velheli = 100
        if helicopter.x >= 6000:
            velheli = -100
        if tiro_helicoptero == True:
            helicopter_bullet.draw()
            helicopter_bullet.x -= 100*janela.delta_time()*variables.dificuldade
            helicopter_bullet.y += 80*janela.delta_time()*variables.dificuldade
            if helicopter_bullet.y >= 600:
               helicopter_bullet.x = 700
               helicopter_bullet.y = 340
               tiro_helicoptero = False
        if (Collision.collided(player, bullet)) and bullet.x >= 410 - bullet.width and abaixado == False:
            nome = input("Insira seu nome: ")
            with open("ranking.txt", 'a') as ranking:
                ranking.write(f"{nome}#{pontos}\n")
            variables.game_state = 1
            cronometropulo = 0
            cont = 0
            cronometroabaixado = 0
            pontos = 0
            bullet.x = - bullet.width
            police_car.x = 1000
            money_bag.x = 1000
            car_item.x = 1000
            inimigos = 0
            sorteioinimigos = 300
            variables.dificuldade = 1
            abaixado = False
            pulo = False
            pulomaximo = False
            player.set_sequence(0,4)
            tiro_helicoptero = False
            helicopter.x = 6000
            player.y = janela.height - player.height
        if (Collision.collided(player, police_car)) and police_car.x <=435 and player.y >=468  or (Collision.collided(playerabaixado, police_car)) and abaixado == True:
            
            nome = input("Insira seu nome: ")
            with open("ranking.txt", 'a') as ranking:
                ranking.write(f"{nome}#{pontos}\n")
            variables.game_state = 1
            cronometropulo = 0
            cont = 0
            cronometroabaixado = 0
            pontos = 0
            bullet.x = - bullet.width
            police_car.x = 1000
            money_bag.x = 1000
            car_item.x = 1000
            inimigos = 0
            sorteioinimigos = 300
            abaixado = False
            pulo = False
            pulomaximo = False
            player.set_sequence(0,4)
            tiro_helicoptero = False
            helicopter.x = 6000
            variables.dificuldade = 1
            player.y = janela.height - player.height
        if (Collision.collided(player, helicopter_bullet)) and helicopter_bullet.x <=435 and player.y >= 468 and helicopter_bullet.x >=400 or (Collision.collided(playerabaixado, helicopter_bullet)) and abaixado == True and helicopter_bullet.y >= 530:
            nome = input("Insira seu nome: ")
            with open("ranking.txt", 'a') as ranking:
                ranking.write(f"{nome}#{pontos}\n")
            variables.game_state = 1
            cronometropulo = 0
            cont = 0
            cronometroabaixado = 0
            pontos = 0
            bullet.x = - bullet.width
            police_car.x = 1000
            money_bag.x = 1000
            car_item.x = 1000
            inimigos = 0
            sorteioinimigos = 300
            abaixado = False
            pulo = False
            pulomaximo = False
            player.set_sequence(0,4)
            tiro_helicoptero = False
            helicopter.x = 6000
            variables.dificuldade = 1
            player.y = janela.height - player.height
        if (Collision.collided(car, bullet)) and immunity == True:
            bullet.x = 0 - bullet.width
            inimigos = 0
        if (Collision.collided(car, police_car)) and immunity == True:
            police_car.x = 1000
            inimigos = 0
        if (Collision.collided(car, helicopter_bullet)) and immunity == True:
            helicopter_bullet.x = 700
            helicopter_bullet.y = 340
            tiro_helicoptero = False
        
        if pontos >= 400 and pontos < 800:
            variables.dificuldade = 2
        elif pontos >= 800 and pontos < 4000:
            variables.dificuldade = 3
        elif pontos >= 4000:
            variables.dificuldade = 4
        
        fundojogo1.x -= 160 * janela.delta_time() * variables.dificuldade
        fundojogo2.x -= 160 * janela.delta_time() * variables.dificuldade
        money_bag.draw()
        bullet.draw()
        car_item.draw()
        police_car.draw()
        helicopter.draw()
        helicopter.update()
        janela.draw_text(str(pontos),100, 0, size=30, color=(200,200,200), font_name="pricedown bl", bold=False, italic=False)
        
    elif variables.game_state == 3:
        ranking = Ranking(janela)
        ranking.update()
        
    elif variables.game_state == 4: # Lógica de sair foi movida para o menu
        janela.close() # Garante que o jogo feche se o estado 4 for chamado de outro lugar
        
    janela.update()
