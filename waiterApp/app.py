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
spec = FlaskPydanticSpec('flask', title='waiterApi')
spec.register(server)
database = TinyDB('storage=MemoryStorage')
c = count()

class QueryProduto(BaseModel):
    id: Optional[int]
    produto: Optional[str]
    valor: Optional [int]

class Produto(BaseModel):
    id:  Optional[int] = Field(default_factory=lambda: next(c))
    produto: str
    valor: int

class Produtos(BaseModel):
    produto: list[Produto]
    count: int


@server.get('/produtos') # rota , endpoint ... rescurso 
@spec.validate(
    query=QueryProduto,
    resp=Response(HTTP_200=Produtos)
    
) #Criando schemas na documentação
def buscar_produtos():
    '''Busca produtos no banco de dados'''  
    query = request.context.query.dict(exclude_none=True)
    todos_os_produtos = database.search(
        Query().fragment(query)
)  
    return jsonify(
        Produtos(
           produtos=todos_os_produtos,
            count=len(todos_os_produtos)
        ).dict()
    )

@server.get('/produto/<int:id>')
@spec.validate(resp=Response(HTTP_200=Produto))
def buscar_produto(id):
    '''Retorna todas as produtos na base de dados.'''
    try:
        pessoa = database.search(Query().id == id)[0]
    except IndexError:
        return{'message': 'Produto not found!'}, 404
    return jsonify(pessoa)

@server.post('/produtos')
@spec.validate(
    body=Request(Produto),resp=Response(HTTP_200=Produto))

def inserir_produto():
    '''insere um produto no banco de dados'''
    body=request.contex.body.dict()
    database.insert(body)
    return body

@server.put('/produtos/<int:id>')
@spec.validate(
    body=Request(Produto), resp=Response(HTTP_201=Produto)
)
def altera_produto(id):
    '''Altera caracteristicas do produto'''
    Produto = Query()
    body = request.context.body.dict()
    database.update(body, Produto.id == id)
    return jsonify(body)

@server.delete('/produto/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def deletar_produto(id):
    '''Remove produto do banco de dados'''
    database.remove(Query().id == id)
    return jsonify({})

server.run()

