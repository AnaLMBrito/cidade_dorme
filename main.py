#python -m venv .venv
#cd .venv/scripts
#cd ../..
#pip install flask
#método 'get' --> solicita dados para o servidor e transmite na tela
#método 'post' --> envia dados para o servidor, finalidade de criar,
#atualizar ou deletar itens de uma tabela
from app import app

#para rodar o site
if __name__=='__main__':
    app.run(debug=True)
