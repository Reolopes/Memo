import tkinter as tk
import random
import time
from tkinter import *
import pygame

pygame.mixer.init()

linhas = 4
colunas = 5
Tamanho_do_cartao_w = 100
Tamanho_do_cartao_h = 100


janela = tk.Tk()
janela.title('Jogo da memória')
janela.geometry('580x620+800+200')
janela.resizable(False, False)
janela.iconbitmap('ico/memo.ico')
janela.configure(bg='gray')


imagens_cartao = ['images/image1.ppm', 'images/image2.ppm', 'images/image3.ppm', 'images/image4.ppm', 'images/image5.ppm', 'images/image6.ppm',
                   'images/image7.ppm', 'images/image8.ppm', 'images/image9.ppm', 'images/image10.ppm' ]

font_letras = ('Arial', 12, 'bold')
cor_letras = '#708090'
cor_fundo = '#90ee90'
n_max_tentativas = 15
inicia_jogo = False

imagens_dict = {}


def imagens_config():
    if linhas * colunas <= len(imagens_cartao) * 2:
        imagens = imagens_cartao * 2
        random.shuffle(imagens)
        grid = []
        for _ in range(linhas):
            linha = []
            for _ in range(colunas):
                image_file = imagens.pop()
                foto = tk.PhotoImage(file=image_file)
                linha.append(foto)
                imagens_dict[foto] = image_file
            grid.append(linha)
        return grid


def exibir_cartoes():
    for linha in range(linhas):
        for coluna in range(colunas):
            cartao = cartoes[linha][coluna]
            cartao.config(image=grid[linha][coluna])
    janela.update()
    time.sleep(3)
    for linha in range(linhas):
        for coluna in range(colunas):
            cartao = cartoes[linha][coluna]
            cartao.config(image=imagem_cartao)
    janela.update()
    
    
match = pygame.mixer.Sound("sounds/correct_target.mp3")
match.set_volume(0.4)
not_match = pygame.mixer.Sound("sounds/wrong_target.mp3")
not_match.set_volume(0.2)
win = pygame.mixer.Sound("sounds/game_win.mp3")
win.set_volume(0.6)
loose = pygame.mixer.Sound("sounds/game_loose.mp3")
loose.set_volume(0.5)


grid = imagens_config()
cartoes = []
cartao_revelado = []
cartas_correspondentes = []
numero_de_tentativas = 0

imagem_cartao = tk.PhotoImage(width=Tamanho_do_cartao_w, height=Tamanho_do_cartao_h)
imagens_conjunto = {}

for image_file in imagens_cartao:
    imagens_conjunto[image_file] = tk.PhotoImage(file=image_file)

def travar_cartoes(cartao1, cartao2):
    cartao1.config(state=tk.DISABLED)
    cartao2.config(state=tk.DISABLED)

def cartao_selecionado(linha, coluna):
    global cartao_revelado, cartas_correspondentes, numero_de_tentativas, inicia_jogo, n_max_tentativas

    if not inicia_jogo:
        return
    
    if inicia_jogo:
        cartao = cartoes[linha][coluna]
        if cartao_revelado == [(linha, coluna)] or (linha, coluna) in cartas_correspondentes:
            return

        cartao.config(image=grid[linha][coluna])
        cartao_revelado.append((linha, coluna))

        if len(cartao_revelado) == 2:
            janela.update()
            time.sleep(0.5)

            imagem1 = imagens_dict[grid[cartao_revelado[0][0]][cartao_revelado[0][1]]]
            imagem2 = imagens_dict[grid[cartao_revelado[1][0]][cartao_revelado[1][1]]]

            if imagem1 == imagem2:
                match.play()
                cartas_correspondentes.extend(cartao_revelado)
            else:
                numero_de_tentativas += 1
                not_match.play()
                label_tentativas.config(text='Tentativas: {}/{}'.format(numero_de_tentativas, n_max_tentativas))
                if numero_de_tentativas == n_max_tentativas:
                    not_match.stop()
                    label_tentativas.config(text='Fim do Jogo. Você perdeu!', bg='#af0000')
                    loose.play()
                    exibir_cartoes()
                    janela.destroy()
                for linha, coluna in cartao_revelado:
                    cartoes[linha][coluna].config(image=imagem_cartao)

            cartao_revelado = []

            if len(cartas_correspondentes) == linhas * colunas:
                match.stop()
                win.play()
                label_tentativas.config(text='Parabéns! Jogo concluído com {} tentativas.'.format(numero_de_tentativas))
                inicia_jogo = False
                
for linha in range(linhas):
    cartao_format = []
    for coluna in range(colunas):
        cartao = tk.Button(janela, width=Tamanho_do_cartao_w, height=Tamanho_do_cartao_h, image=imagem_cartao,
                           command=lambda r=linha, c=coluna: cartao_selecionado(r, c))
        cartao.grid(row=linha, column=coluna, padx=5, pady=5)
        cartao_format.append(cartao)
    cartoes.append(cartao_format)

button_style = {'activebackground': '#f8f9fa', 'font': font_letras}

label_tentativas = tk.Label(janela, text='Tentativas: {}/{}'.format(numero_de_tentativas, n_max_tentativas),
                            fg=cor_letras, bg=cor_fundo, font=font_letras)
label_tentativas.grid(row=linhas, columnspan=colunas, padx=30, pady=40)


def bloquear_cartoes():
    for linha in range(linhas):
        for coluna in range(colunas):
            cartoes[linha][coluna].config(state=tk.DISABLED)

bloquear_cartoes()

def desbloquear_cartoes():
    for linha in range(linhas):
        for coluna in range(colunas):
            cartoes[linha][coluna].config(state=tk.NORMAL)

def inicia_jogo():
    global inicia_jogo, cartao
    inicia_jogo = True
    if inicia_jogo:
        start_button.destroy()
        desbloquear_cartoes()
        exibir_cartoes()
        
        
start_button = tk.Button(janela, text="Iniciar Jogo", command=inicia_jogo)
start_button.grid(row=linhas + 1, columnspan=colunas, padx=10, pady=0)


janela.mainloop()
