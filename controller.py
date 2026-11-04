# ============================================================
# CONTROLLER (Lógica do sistema)
# Recebe as requisições do navegador, aplica as regras de negócio,
# conversa com o Model e escolhe qual View devolver.
# ============================================================
from datetime import date, datetime
from flask import render_template, request, redirect, url_for, flash
from model import db, Gasto, CATEGORIAS


def calcular_resumo(gastos):
    """Regra de negócio: totais geral, pago, pendente e por categoria."""
    total = sum(g.valor for g in gastos)
    pago = sum(g.valor for g in gastos if g.pago)
    por_categoria = {}
    for g in gastos:
        por_categoria[g.categoria] = por_categoria.get(g.categoria, 0) + g.valor
    # Ordena da categoria que mais gastou para a que menos gastou
    por_categoria = dict(sorted(por_categoria.items(), key=lambda item: item[1], reverse=True))
    return {"total": total, "pago": pago, "pendente": total - pago, "por_categoria": por_categoria}


def validar_formulario(form):
    """Regra de negócio: valida os dados antes de salvar. Devolve (dados, erro)."""
    descricao = form.get("descricao", "").strip()
    categoria = form.get("categoria", "Outros")
    try:
        valor = float(form.get("valor", "0").replace(",", "."))
    except ValueError:
        return None, "Informe um valor numérico válido."
    if not descricao:
        return None, "A descrição é obrigatória."
    if valor <= 0:
        return None, "O valor precisa ser maior que zero."
    if categoria not in CATEGORIAS:
        categoria = "Outros"
    try:
        data_gasto = datetime.strptime(form.get("data", ""), "%Y-%m-%d").date()
    except ValueError:
        data_gasto = date.today()
    return {"descricao": descricao, "valor": valor, "categoria": categoria, "data": data_gasto}, None


def rotas(app):
    @app.route("/")  # Rota principal: lista os gastos (com filtro opcional por categoria)
    def index():
        filtro = request.args.get("categoria", "")
        consulta = Gasto.query.order_by(Gasto.data.desc(), Gasto.id.desc())
        if filtro in CATEGORIAS:
            consulta = consulta.filter_by(categoria=filtro)
        gastos = consulta.all()
        resumo = calcular_resumo(gastos)
        return render_template("index.html", gastos=gastos, resumo=resumo,
                               categorias=CATEGORIAS, filtro=filtro, hoje=date.today().isoformat())

    @app.route("/adicionar", methods=["POST"])  # Recebe o formulário e cadastra um gasto
    def adicionar():
        dados, erro = validar_formulario(request.form)
        if erro:
            flash(erro)
            return redirect(url_for("index"))
        db.session.add(Gasto(**dados))
        db.session.commit()  # Grava no banco
        flash("Gasto cadastrado!")
        return redirect(url_for("index"))

    @app.route("/editar/<int:id>", methods=["GET", "POST"])  # Mostra e salva a edição
    def editar(id):
        gasto = db.get_or_404(Gasto, id)
        if request.method == "POST":
            dados, erro = validar_formulario(request.form)
            if erro:
                flash(erro)
                return redirect(url_for("editar", id=id))
            for campo, valor in dados.items():
                setattr(gasto, campo, valor)
            db.session.commit()
            flash("Gasto atualizado!")
            return redirect(url_for("index"))
        return render_template("editar.html", gasto=gasto, categorias=CATEGORIAS)

    @app.route("/pagar/<int:id>")  # Alterna o status pago / pendente
    def pagar(id):
        gasto = db.get_or_404(Gasto, id)
        gasto.pago = not gasto.pago
        db.session.commit()
        return redirect(request.referrer or url_for("index"))

    @app.route("/deletar/<int:id>")  # Exclui o gasto
    def deletar(id):
        gasto = db.get_or_404(Gasto, id)
        db.session.delete(gasto)
        db.session.commit()
        flash("Gasto excluído.")
        return redirect(request.referrer or url_for("index"))
