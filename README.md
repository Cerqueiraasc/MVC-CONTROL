# Troco: controle de gastos (Prática MVC com Flask)

**Dupla:** Arthur Silva de Cerqueira e Elias Viana
**Disciplina:** Modelos, Métodos e Técnicas da Engenharia de Software — Aula 8

Aplicação web para registrar gastos pessoais, marcar como pagos, filtrar por categoria e ver os totais. Feita em Python com Flask + SQLite, organizada na arquitetura **MVC**.

## Funcionalidades
- Cadastrar gasto (descrição, valor, categoria e data)
- Visualizar gastos em tabela, do mais recente ao mais antigo
- Editar gasto
- Marcar como pago / pendente
- Excluir gasto
- Filtrar por categoria
- Resumo: total, pago, pendente e total por categoria

## Como o MVC foi aplicado

| Camada | Arquivo | Função no projeto |
|---|---|---|
| **Model** | `model.py` | Classe `Gasto` (tabela no banco SQLite) e lista de categorias |
| **Controller** | `controller.py` | Rotas (`/`, `/adicionar`, `/editar`, `/pagar`, `/deletar`), validação dos dados e cálculo dos totais |
| **View** | `templates/*.html` + `static/style.css` | Interface HTML que só exibe o que o Controller entrega |
| Servidor | `server.py` | Cria o app Flask, conecta o banco, cria as tabelas e registra as rotas |

Fluxo: o navegador faz uma requisição → o **Controller** recebe, valida e consulta/grava no **Model** → o Controller calcula os totais e chama a **View** (`render_template`) → o HTML volta para o navegador.

Exemplo de regra de negócio no Controller: um gasto só é salvo se tiver descrição e valor maior que zero; caso contrário, aparece uma mensagem de aviso.

## Estrutura
```
controle-gastos/
├── server.py
├── model.py
├── controller.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── editar.html
└── static/
    ├── logo.svg
    └── style.css
```

## Como executar no Replit
1. Crie um Repl Python e envie todos os arquivos mantendo as pastas `templates` e `static`.
2. No Shell: `pip install flask flask-sqlalchemy`
3. Crie o Workflow: nova aba → **Workflow** → **New Workflow** → nome "Execução" → Mode **Sequential** → Task **Execute Shell Command**: `python server.py` → Salvar.
4. Clique em **Run**. O banco `gastos.db` é criado dentro da pasta `instance` (dá para abrir em https://sqliteviewer.app/).

Para rodar no computador: `pip install flask flask-sqlalchemy` e `python server.py`, depois acesse http://localhost:5000.
