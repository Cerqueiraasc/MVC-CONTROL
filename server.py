# ============================================================
# SERVER: inicia o servidor, conecta ao banco e cria as tabelas
# ============================================================
from flask import Flask
from model import db
from controller import rotas

app = Flask(__name__)  # Cria a aplicação Flask

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gastos.db"  # Banco SQLite (fica na pasta instance)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False             # Evita avisos desnecessários
app.config["SECRET_KEY"] = "trabalho-mvc"                        # Necessário para as mensagens (flash)

db.init_app(app)  # Conecta o banco à aplicação

with app.app_context():
    db.create_all()  # Cria as tabelas, se ainda não existirem

@app.template_filter("brl")  # Filtro usado na View para mostrar valores como R$ 1.234,56
def formatar_brl(valor):
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

rotas(app)  # Registra as rotas definidas no controller

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Acessível em todas as interfaces na porta 5000
