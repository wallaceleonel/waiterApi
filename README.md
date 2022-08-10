# Desenvolvendo  uma api seguindo os padrões RESTful

Neste projeto usamos uma nova stack e a implementação de uma nova arquitetura segundo os pradrões Rest para criação de api´s

## Stacks usadas 

- Flask 
- Flas-pydantic-spec
- TinyDB
- pydantic
- werkzeug
## Api documentada no Swagger

 <img src= "waiterApp\media\swagger.PNG" align="center">
 <img src= "waiterApp\media\schemas.PNG" align="center">


 ## Rodando aplicação 

executar criação de ambiente virutal em python 
 ````sh
    python -m env nomeDoAmbiente
 ````
 execução do ambiente 
 ````sh
    source env/nomeDoAmbiente/Scripts/activate
 ````
 com ambiente criado, precisara instalar pacotes do flask e baco de dados 
 ````sh
    pip install flask
    pip install flask-pydantic-spec
    pip install tinydb
    pip install werkzeug==2.1.2
 ````
com as depencencias instaladas precisara exporta projeto para flask 
````sh 
export FLASK_APP=app.py
````
Rodando projeto 
`````sh
flask run
`````
