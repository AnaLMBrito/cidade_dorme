from flask import Flask, render_template, request, redirect, url_for, session, flash
from bd import gerar_jogadores_e_papeis
#url_for - função que renderiza a página a 
#partir do nome da função, independente do nome da rota
#{{url_for('')}} 
#session - permite guardar informações entre páginas
#flash - envia mensagens rápidas para o usuário
#Importa do arquivo bd.py a função que sorteia os jogadores

#Cria o app Flask
#secret_key - permite a utilização da sessão e flash
app = Flask(__name__)
app.secret_key = "senha123"

#renderiza index (página incial) com botões para login e regras
@app.route("/")
def index():
    return render_template("index.html")

#mostra/traz a página ddas regras do jogo ao ser clicado o botão de regras na página inicial
@app.route("/regras")
def regras():
    return render_template("regras.html")

#GET - mostrar a página 
#POST - receber formulário
@app.route("/login", methods=["GET", "POST"])
def login():
    #pega o nome digitado pelo usuário
    if request.method == "POST":
        nome = request.form.get("nome")
        #se o campo nome estiver vazio ou não atender aos requisitos de validação (pelo menos 2 caracteres e pelo menos uma letra) retorna uma mensagem flash e recarrega para uma nova tentativa.
        #o for vai percorrer cada caractere para ver se tem alguma letra.
        if not nome or len(nome) < 2 or not any(c.isalpha() for c in nome):
            flash("Erro. Digite um nome com pelo menos 2 caracteres e pelo menos uma letra.")
            return redirect(url_for("login"))

        #salva o nome na sessão
        session["nome"] = nome
        #vai para a página de sorteio de papeis
        return redirect(url_for("sorteio"))
    
    #renderiza a página login
    return render_template("login.html")


@app.route("/reset")
def reset():
    #limpa sessão e volta para a página inicial, "reiniciando" o site
    session.clear()
    return redirect(url_for("index"))

#a partir do botão iniciar partida, pega o sorteio e redireciona o usuario para seu respectivo papel
@app.route("/sorteio", methods=["GET", "POST"])
def sorteio():
    #verifica se o usuario está logado em uma sessão (não digitou /sorteio na barra, por exemplo), se não estiver, é redirecionado para login.
    if "nome" not in session:
        flash("É necessário login para jogar, faça seu login!")
        return redirect(url_for("login"))

    #se o botão "Iniciar partida" for clicado
    if request.method == "POST":
        #pega a lista de jogadores e os respectivos papeis através da função criada no bd.py
        jogadores, papeis = gerar_jogadores_e_papeis(session["nome"])

        #guarda o nome dos jogadores na sessão do usuário, o que permite acessar a lista em outras páginas durante o jogo, sem precisar passar pela função novamente.
        session["jogadores"] = jogadores
        #guarda na sessão também o papel do jogador usuário para ter a experiência personalizada de acordo com o seu papel
        session["papel"] = papeis[session["nome"]]

        #redireciona para a página correspondente ao papel sorteado
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
    if "papel" not in session or session["papel"] != "assassino":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))

    jogadores = [j for j in session.get("jogadores", []) if j != session["nome"]]

    if request.method == "POST":
        vitima = request.form.get("vitima")
        session["vitima"] = vitima
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
    if "papel" not in session or session["papel"] != "anjo":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))

    return render_template("anjo_espera.html")

@app.route("/anjo", methods=["GET", "POST"])
def anjo():
    if "papel" not in session or session["papel"] != "anjo":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))

    jogadores = session.get("jogadores", [])

    if request.method == "POST":
        salvo = request.form.get("salvo")
        session["salvo"] = salvo
        return redirect(url_for("votacao"))

    return render_template("anjo.html", jogadores=jogadores)

@app.route("/cidadao_mensagem")
def cidadao_mensagem():
    if "papel" not in session or session["papel"] != "cidadao":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))

    return render_template("cidadao_mensagem.html")

@app.route("/cidadao_espera")
def cidadao_espera():
    if "papel" not in session or session["papel"] != "cidadao":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))

    return render_template("cidadao_espera.html")

@app.route("/cidadao")
def cidadao():
    if "papel" not in session or session["papel"] != "cidadao":
        flash("Acesso negado!")
        return redirect(url_for("sorteio"))

    jogadores = session.get("jogadores", [])
    return render_template("cidadao.html", jogadores=jogadores)

@app.route("/votacao", methods=["GET", "POST"])
def votacao():
    if "nome" not in session:
        flash("É necessário login para votar!")
        return redirect(url_for("login"))

    jogadores = session.get("jogadores", [])
    if request.method == "POST":
        voto = request.form.get("votacao")
        session["voto"] = voto
        return redirect(url_for("resultado"))

    return render_template("votacao.html", jogadores=jogadores)

@app.route("/resultado")
def resultado():
    return render_template("resultado.html")

#para rodar o site
if __name__=='__main__':
    app.run(debug=True)