import random
import tkinter as tk
from tkinter import messagebox

def criar_tabuleiro(linhas, colunas, num_bombas):
    # Cria um tabuleiro vazio com o número de linhas e colunas especificado
    tabuleiro = [[' ' for _ in range(colunas)] for _ in range(linhas)]
    
    # Coloca as bombas no tabuleiro de forma aleatória
    bombas_colocadas = 0
    while bombas_colocadas < num_bombas:
        x = random.randint(0, linhas - 1)
        y = random.randint(0, colunas - 1)
        if tabuleiro[x][y] != 'B':
            tabuleiro[x][y] = 'B'
            bombas_colocadas += 1
    
    # Preenche os números indicando o número de bombas adjacentes
    for i in range(linhas):
        for j in range(colunas):
            if tabuleiro[i][j] != 'B':
                bombas_adjacentes = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= i + dx < linhas and 0 <= j + dy < colunas and tabuleiro[i + dx][j + dy] == 'B':
                            bombas_adjacentes += 1
                if bombas_adjacentes > 0:
                    tabuleiro[i][j] = str(bombas_adjacentes)
    
    return tabuleiro

def revelar_celula(tabuleiro, tabuleiro_mostrado, linhas, colunas, x, y):
    if x < 0 or x >= linhas or y < 0 or y >= colunas:
        return
    if tabuleiro_mostrado[x][y] != ' ':
        return
    tabuleiro_mostrado[x][y] = tabuleiro[x][y]

    if tabuleiro[x][y] == 'B':
        return

    if tabuleiro[x][y] == ' ':
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                revelar_celula(tabuleiro, tabuleiro_mostrado, linhas, colunas, x + dx, y + dy)

def jogar():
    root = tk.Tk()
    root.title("Campo Minado")

    linhas = int(input("Digite o número de linhas do tabuleiro: "))
    colunas = int(input("Digite o número de colunas do tabuleiro: "))
    num_bombas = int(input("Digite o número de bombas: "))

    tabuleiro = criar_tabuleiro(linhas, colunas, num_bombas)
    tabuleiro_mostrado = [[' ' for _ in range(colunas)] for _ in range(linhas)]
    jogadas_restantes = linhas * colunas - num_bombas

    def click_celula(x, y):
        if tabuleiro_mostrado[x][y] != ' ':
            return

        if tabuleiro[x][y] == 'B':
            messagebox.showinfo("Fim de jogo", "Você encontrou uma bomba! Fim de jogo!")
            root.quit()
            return

        revelar_celula(tabuleiro, tabuleiro_mostrado, linhas, colunas, x, y)
        nonlocal jogadas_restantes
        jogadas_restantes -= 1
        if jogadas_restantes == 0:
            messagebox.showinfo("Parabéns!", "Você venceu!")
            root.quit()

        atualizar_tabuleiro()

    def atualizar_tabuleiro():
        for x in range(linhas):
            for y in range(colunas):
                celula = tabuleiro_mostrado[x][y]
                if celula == ' ':
                    button_texts[x][y].config(text='', state=tk.NORMAL)
                else:
                    button_texts[x][y].config(text=celula, state=tk.DISABLED)

    button_texts = [[None for _ in range(colunas)] for _ in range(linhas)]

    for x in range(linhas):
        for y in range(colunas):
            button = tk.Button(root, width=3, height=1, command=lambda x=x, y=y: click_celula(x, y))
            button.grid(row=x, column=y)
            button_texts[x][y] = button

    root.mainloop()

if __name__ == "__main__":
    jogar()
