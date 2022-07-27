from itertools import count
from typing import Optional

from flask import Flask, request, jsonify
from flask_pydantic_spec import (
    FlaskPydanticSpec, Response, Request
)
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage


server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Waiter Api ')
spec.register(server)
database = TinyDB(storage=MemoryStorage)
c = count()


class QueryProduto(BaseModel):
    id: Optional[int]
    nome: Optional[str]
    valor: Optional[int]


class Produto(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
    nome: str
    valor: int


class Produtos(BaseModel):
    produto: list[Produto]
    count: int


@server.get('/produtos')  # Rota, endpoint, recurso ...
@spec.validate(
    query=QueryProduto,
    resp=Response(HTTP_200=Produtos)
)
def buscar_produtos():
    """Retorna todos os Produtos da base de dados."""
    query = request.context.query.dict(exclude_none=True)
    todos_os_produtos = database.search(
        Query().fragment(query)
    )
    return jsonify(
        Produtos(
            pessoas=todos_os_produtos,
            count=len(todos_os_produtos)
        ).dict()
    )

@server.get('/produtos/<int:id>')
@spec.validate(resp=Response(HTTP_200=Produto))
def buscar_produto(id):
    """Retorna   Produtos cujo Id foi informado  da base de dados."""
    try:
        produto = database.search(Query().id == id)[0]
    except IndexError:
        return {'message': 'Produto not found!'}, 404
    return jsonify(produto)


@server.post('/produtos')
@spec.validate(
    body=Request(Produto), resp=Response(HTTP_201=Produto)
)
def inserir_produto():
    """Insere um Produto no banco de dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body


@server.put('/produtos/<int:id>')
@spec.validate(
    body=Request(Produto), resp=Response(HTTP_201=Produto)
)
def altera_produto(id):
    """Altera um Produto no banco de dados."""
    Produto = Query()
    body = request.context.body.dict()
    database.update(body, Produto.id == id)
    return jsonify(body)


@server.delete('/produtos/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def deleta_produto(id):
    """Remove um Produto do banco de dados."""
    database.remove(Query().id == id)
    return jsonify({})


server.run()