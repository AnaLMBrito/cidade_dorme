#arquivo de inicialização do módulo 'app'
from flask import Flask

app = Flask(__name__)



#para não dar erro temos que importar as rotas
from app.routes import home