from flask import Flask, render_template, request, redirect, url_for, session, flash
from bd import gerar_jogadores_e_papeis
import random

app = Flask(__name__)
app.secret_key = "senha123"

# Variáveis globais para gerenciar o estado do jogo
estado_jogo = {
    "vitima": None,
    "salvo": None,
    "votos": {},
    "jogadores_vivos": [],
    "papeis_globais": {},
    "ultimo_eliminado": None,
    "papel_eliminado": None,
    "assassino_nome": None,
    "anjo_nome": None
}

def bot_assassino_escolhe_vitima():
    """Bot assassino escolhe uma vítima aleatória"""
    global estado_jogo
    assassino = estado_jogo.get("assassino_nome")
    
    # Lista de jogadores vivos exceto o assassino
    possiveis_vitimas = [j for j in estado_jogo["jogadores_vivos"] if j != assassino]
    
    if possiveis_vitimas:
        vitima = random.choice(possiveis_vitimas)
        estado_jogo["vitima"] = vitima
        return vitima
    return None

def bot_anjo_escolhe_salvo():
    """Bot anjo escolhe alguém aleatório para salvar"""
    global estado_jogo
    
    # Anjo pode escolher qualquer jogador vivo (incluindo ele mesmo)
    jogadores_vivos = estado_jogo["jogadores_vivos"]
    
    if jogadores_vivos:
        salvo = random.choice(jogadores_vivos)
        estado_jogo["salvo"] = salvo
        return salvo
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/regras")
def regras():
    return render_template("regras.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form.get("nome")
        if not nome or len(nome) < 2 or not any(c.isalpha() for c in nome):
            flash("Erro. Digite um nome com pelo menos 2 caracteres e pelo menos uma letra.")
            return redirect(url_for("login"))

        session["nome"] = nome
        return redirect(url_for("sorteio"))
    
    return render_template("login.html")

@app.route("/reset")
def reset():
    global estado_jogo
    session.clear()
    estado_jogo = {
        "vitima": None,
        "salvo": None,
        "votos": {},
        "jogadores_vivos": [],
        "papeis_globais": {},
        "ultimo_eliminado": None,
        "papel_eliminado": None,
        "assassino_nome": None,
        "anjo_nome": None
    }
    return redirect(url_for("index"))

@app.route("/sorteio", methods=["GET", "POST"])
def sorteio():
    global estado_jogo
    
    if "nome" not in session:
        flash("É necessário login para jogar, faça seu login!")
        return redirect(url_for("login"))

    if request.method == "POST":
        jogadores, papeis = gerar_jogadores_e_papeis(session["nome"])

        session["jogadores"] = jogadores
        session["papel"] = papeis[session["nome"]]
        
        # Inicializa o estado global do jogo
        estado_jogo["jogadores_vivos"] = jogadores.copy()
        estado_jogo["papeis_globais"] = papeis
        estado_jogo["votos"] = {}
        estado_jogo["ultimo_eliminado"] = None
        estado_jogo["papel_eliminado"] = None
        
        # Identifica quem é o assassino e quem é o anjo
        for jogador, papel in papeis.items():
            if papel == "assassino":
                estado_jogo["assassino_nome"] = jogador
            elif papel == "anjo":
                estado_jogo["anjo_nome"] = jogador

        papel = session["papel"]
        if papel == "assassino":
            return redirect(url_for("assassino_mensagem"))
        elif papel == "anjo":
            return redirect(url_for("anjo_mensagem"))
        elif papel == "cidadao":
            return redirect(url_for("cidadao_mensagem"))

    return render_template("sorteio.html")

@app.route("/assassino_mensagem")
def assassino_mensagem():
    if "papel" not in session or session["papel"] != "assassino":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))
    return render_template("assassino_mensagem.html")

@app.route("/assassino", methods=["GET", "POST"])
def assassino():
    global estado_jogo
    
    if "papel" not in session or session["papel"] != "assassino":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))

    jogadores = [j for j in estado_jogo["jogadores_vivos"] if j != session["nome"]]

    if request.method == "POST":
        vitima = request.form.get("vitima")
        estado_jogo["vitima"] = vitima
        
        # Bot anjo escolhe alguém para salvar
        anjo = estado_jogo.get("anjo_nome")
        if anjo and anjo.startswith("Bot") and anjo in estado_jogo["jogadores_vivos"]:
            bot_anjo_escolhe_salvo()
        
        return redirect(url_for("assassino_durma"))

    return render_template("assassino.html", jogadores=jogadores)

@app.route("/assassino_durma")
def assassino_durma():
    if "papel" not in session or session["papel"] != "assassino":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))
    return render_template("assassino_durma.html")

@app.route("/anjo_mensagem")
def anjo_mensagem():
    if "papel" not in session or session["papel"] != "anjo":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))
    return render_template("anjo_mensagem.html")

@app.route("/anjo_espera")
def anjo_espera():
    global estado_jogo
    
    if "papel" not in session or session["papel"] != "anjo":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))
    
    # Bot assassino escolhe uma vítima
    assassino = estado_jogo.get("assassino_nome")
    if assassino and assassino.startswith("Bot") and assassino in estado_jogo["jogadores_vivos"]:
        if not estado_jogo.get("vitima"):
            bot_assassino_escolhe_vitima()
    
    return render_template("anjo_espera.html")

@app.route("/anjo", methods=["GET", "POST"])
def anjo():
    global estado_jogo
    
    if "papel" not in session or session["papel"] != "anjo":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))

    jogadores = estado_jogo["jogadores_vivos"]

    if request.method == "POST":
        salvo = request.form.get("salvo")
        estado_jogo["salvo"] = salvo
        return redirect(url_for("resultado_noite"))

    return render_template("anjo.html", jogadores=jogadores)

@app.route("/cidadao_mensagem")
def cidadao_mensagem():
    if "papel" not in session or session["papel"] != "cidadao":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))
    return render_template("cidadao_mensagem.html")

@app.route("/cidadao_espera")
def cidadao_espera():
    global estado_jogo
    
    if "papel" not in session or session["papel"] != "cidadao":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))
    
    # Bot assassino escolhe uma vítima
    assassino = estado_jogo.get("assassino_nome")
    if assassino and assassino.startswith("Bot") and assassino in estado_jogo["jogadores_vivos"]:
        if not estado_jogo.get("vitima"):
            bot_assassino_escolhe_vitima()
    
    # Bot anjo escolhe alguém para salvar
    anjo = estado_jogo.get("anjo_nome")
    if anjo and anjo.startswith("Bot") and anjo in estado_jogo["jogadores_vivos"]:
        if not estado_jogo.get("salvo"):
            bot_anjo_escolhe_salvo()
    
    return render_template("cidadao_espera.html")

@app.route("/resultado_noite")
def resultado_noite():
    global estado_jogo
    
    if "nome" not in session:
        flash("É necessário login!")
        return redirect(url_for("login"))
    
    # Garante que bot assassino escolheu se necessário
    assassino = estado_jogo.get("assassino_nome")
    if assassino and assassino.startswith("Bot") and assassino in estado_jogo["jogadores_vivos"]:
        if not estado_jogo.get("vitima"):
            bot_assassino_escolhe_vitima()
    
    # Garante que bot anjo escolheu se necessário
    anjo = estado_jogo.get("anjo_nome")
    if anjo and anjo.startswith("Bot") and anjo in estado_jogo["jogadores_vivos"]:
        if not estado_jogo.get("salvo"):
            bot_anjo_escolhe_salvo()
    
    vitima = estado_jogo.get("vitima")
    salvo = estado_jogo.get("salvo")
    morto = None
    mensagem = ""
    
    # Verifica se alguém morreu
    if vitima and vitima != salvo:
        morto = vitima
        if morto in estado_jogo["jogadores_vivos"]:
            estado_jogo["jogadores_vivos"].remove(morto)
        mensagem = f"O assassino atacou {vitima}!"
    elif vitima and vitima == salvo:
        mensagem = f"O anjo salvou {salvo}! Ninguém morreu."
    else:
        mensagem = "A noite passou tranquila."
    
    # Reseta as escolhas da noite
    estado_jogo["vitima"] = None
    estado_jogo["salvo"] = None
    
    return render_template("resultado.html", mensagem=mensagem, morto=morto)

@app.route("/votacao", methods=["GET", "POST"])
def votacao():
    global estado_jogo
    
    if "nome" not in session:
        flash("É necessário login para votar!")
        return redirect(url_for("login"))
    
    # Verifica se o jogador está vivo
    if session["nome"] not in estado_jogo["jogadores_vivos"]:
        flash("Você foi eliminado e não pode mais votar!")
        return redirect(url_for("index"))

    jogadores = estado_jogo["jogadores_vivos"]
    
    if request.method == "POST":
        voto = request.form.get("votacao")
        
        # Validação: assassino não pode votar nele mesmo
        if session["papel"] == "assassino" and voto == session["nome"]:
            flash("Você não pode votar em si mesmo!")
            return redirect(url_for("votacao"))
        
        # Registra o voto do usuário
        estado_jogo["votos"][session["nome"]] = voto
        
        # Bots votam automaticamente
        for jogador in estado_jogo["jogadores_vivos"]:
            if jogador.startswith("Bot") and jogador not in estado_jogo["votos"]:
                # Cria lista de possíveis votos (exceto o próprio bot)
                possiveis_votos = [j for j in estado_jogo["jogadores_vivos"] if j != jogador]
                
                # Se o bot for o assassino, não pode votar nele mesmo
                if estado_jogo["papeis_globais"].get(jogador) == "assassino":
                    possiveis_votos = [j for j in possiveis_votos if j != jogador]
                
                if possiveis_votos:
                    estado_jogo["votos"][jogador] = random.choice(possiveis_votos)
        
        return redirect(url_for("aguardando_votacao"))

    return render_template("votacao.html", jogadores=jogadores)

@app.route("/aguardando_votacao")
def aguardando_votacao():
    if "nome" not in session:
        flash("É necessário login!")
        return redirect(url_for("login"))
    
    return render_template("aguardando_votacao.html")

@app.route("/resultado_votacao")
def resultado_votacao():
    global estado_jogo
    
    if "nome" not in session:
        flash("É necessário login!")
        return redirect(url_for("login"))
    
    # Conta os votos
    contagem = {}
    for votante, votado in estado_jogo["votos"].items():
        if votado in contagem:
            contagem[votado] += 1
        else:
            contagem[votado] = 1
    
    # Encontra quem recebeu mais votos
    if contagem:
        eliminado = max(contagem, key=contagem.get)
        votos_recebidos = contagem[eliminado]
        
        if eliminado in estado_jogo["jogadores_vivos"]:
            estado_jogo["jogadores_vivos"].remove(eliminado)
        
        # Verifica se o eliminado era o assassino
        papel_eliminado = estado_jogo["papeis_globais"].get(eliminado)
        
        # Guarda informações do eliminado
        estado_jogo["ultimo_eliminado"] = eliminado
        estado_jogo["papel_eliminado"] = papel_eliminado
        
        # Limpa os votos para a próxima rodada
        estado_jogo["votos"] = {}
        
        # Mostra o resultado da votação
        return render_template("resultado_votacao.html", 
                             eliminado=eliminado, 
                             papel=papel_eliminado,
                             votos=votos_recebidos)
    
    # Se não houver votos, continua o jogo
    return render_template("resultado_votacao.html", eliminado=None, papel=None, votos=0)

@app.route("/verificar_vitoria")
def verificar_vitoria():
    global estado_jogo
    
    if "nome" not in session:
        flash("É necessário login!")
        return redirect(url_for("login"))
    
    papel_eliminado = estado_jogo.get("papel_eliminado")
    
    # Verifica se o assassino foi eliminado
    if papel_eliminado == "assassino":
        return redirect(url_for("fim_cidade"))
    
    # Conta quantos cidadãos (incluindo anjo) restam
    vivos_nao_assassinos = sum(1 for j in estado_jogo["jogadores_vivos"] 
                               if estado_jogo["papeis_globais"].get(j) != "assassino")
    
    # Se sobrar só o assassino e mais um, assassino vence
    if vivos_nao_assassinos <= 1:
        return redirect(url_for("fim_assassino"))
    
    # Continua o jogo - volta para a noite
    if session["nome"] not in estado_jogo["jogadores_vivos"]:
        # Jogador foi eliminado
        flash("Você foi eliminado!")
        return redirect(url_for("index"))
    
    # Jogador continua vivo, volta para seu papel
    if session["papel"] == "assassino":
        return redirect(url_for("assassino"))
    elif session["papel"] == "anjo":
        return redirect(url_for("anjo_espera"))
    elif session["papel"] == "cidadao":
        return redirect(url_for("cidadao_espera"))

@app.route("/fim_cidade")
def fim_cidade():
    return render_template("fim_cidade.html")

@app.route("/fim_assassino")
def fim_assassino():
    return render_template("fim_assassino.html")

if __name__=='__main__':
    app.run(debug=True)