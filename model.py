# ============================================================
# MODEL (Banco / Acesso a dados)
# Define a estrutura dos dados e como eles são guardados no banco.
# ============================================================
from datetime import date
from flask_sqlalchemy import SQLAlchemy  # Extensão que permite usar banco relacional com Flask

db = SQLAlchemy()  # Instância do SQLAlchemy usada para interagir com o banco de dados

# Categorias disponíveis para classificar os gastos
CATEGORIAS = ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Educação", "Outros"]


class Gasto(db.Model):  # Classe "Gasto", que representa a tabela "gasto" no banco
    id = db.Column(db.Integer, primary_key=True)          # Chave primária
    descricao = db.Column(db.String(120), nullable=False)  # Ex.: "Almoço", "Uber"
    valor = db.Column(db.Float, nullable=False)            # Valor em reais
    categoria = db.Column(db.String(30), nullable=False, default="Outros")
    data = db.Column(db.Date, nullable=False, default=date.today)
    pago = db.Column(db.Boolean, default=False)            # Se o gasto já foi pago

    def __repr__(self):
        return f"<Gasto {self.descricao} - R$ {self.valor:.2f}>"
