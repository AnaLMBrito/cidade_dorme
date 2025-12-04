import random
#random - sorteio, será responsável por embaralhar listas e sortear papéis.

#função que recebe o nome do jogador de app.py
#lista com os 15 jogadores (jogador real + 14 bots)
#dicionário com papel de cada jogador
def gerar_jogadores_e_papeis(nome_jogador):
    #lista de jogadores que terá o nome do jogador real mais o dos bots (bot1, ...)
    jogadores = [nome_jogador]
    #f-string - tipo de string onde você pode colocar variáveis diretamente dentro do texto, que nem print.
    for i in range(1, 15):
        jogadores.append(f"Bot{i}")

    #shuffle - é um modulo do random, que vai mudar a ordem dos elementos da lista, embaralhando-a
    random.shuffle(jogadores)

    #dicionário vazio que depois ficará com "jogador" : "papel"
    papeis = {}

    #assassino - variável que, a partir do random.chocie (escolha aleatória), pegará um jogador aleatoriamente para ser o assassino.
    assassino = random.choice(jogadores)
    #elemento "nome_do_jogador" : "assassino" adicionado ao dicionário
    papeis[assassino] = "assassino"

    #j - variávl temporária usada para percorrer a lista de jogadores para adicionar todos à lista 'restantes', menos o assassino.
    restantes = []
    for j in jogadores:
        if j != assassino:
            restantes.append(j)

    #escolhe um jogador da lista restante aleatoriamente paara ser o anjo, mesmo esquema do assassino só que "outro_jogador" : "anjo".
    anjo = random.choice(restantes)
    papeis[anjo] = "anjo"

    #se o  jogador não estiver no dicionário de papeis, ele será adicionado ao dicionário commo jogador "jogador" : "cidadao"
    for j in jogadores:
        if j not in papeis:
            papeis[j] = "cidadao"
            
    #retorna o nome dos jogadores e os papeis de cada um.
    return jogadores, papeis


        