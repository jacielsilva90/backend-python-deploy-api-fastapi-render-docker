from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
app = FastAPI()
# Modelos Pydantic (Objeto)
class Cidade(BaseModel):
  id: int 
  nome: str
  uf: str
class NovaCidade(BaseModel):
  #id
  nome: str
  uf: str
class Animal(BaseModel):
   id:Optional[int]
   nome:str
   idade:int
   sexo:str
   cor:str
#o frontend aciona o backend por url
# Endpoints=rota=path
# Banco de Dados (local)
id=1
dados = [{"id": 1, "nome": "Teresina", "uf": "PI"},{"id": 2, "nome": "Parnaíba", "uf": "PI"}]
cidads = [Cidade(**item) for item in dados] #asteriscos obrigatorio
#cidades é lista de objetos da classe Cidade
cidades=[Cidade(id=3, nome="The", uf="PI"),Cidade(id=4, nome="picos", uf="PI")]
atual_id=id
bancoc:List[Cidade]=[]
banco:List[Animal]=[]

# @app = decorator
@app.get('/') #rota url raiz root: http://127.0.0.1:8000/
async def root():
    return 'Home - fastapi'
@app.get('/cidads') # url: http://127.0.0.1:8000/cidads
async def cidads_listar():
    return cidads
@app.get('/cidades') #url: http://127.0.0.1:8000/cidades
def cidades_list():
    return cidades

#path paramet = parametro de rota
@app.get('/cidades/{id}')  # http://127.0.0.1:8000/cidades/id
def cidades_detail(id: int):
  for cidade in cidades:
    #id é um atributo de Cidade
    if cidade.id == id:
      return cidade
  return f'Não existe cidade com id {id}'

#path paramet = parametro de rota
@app.get('/elevado_a2/{numero}')
def elevado_a2(numero:int):
    retorno=numero*numero
    texto=f'O quadrado de {numero} é {retorno}'
    return texto
#query paramet = parametro de consulta
@app.get('/area') # http://127.0.0.1:8000/area?a=4&b=5
def area(a:int,b:int=2):
    resul=a*b
    return {'resultado': f'area de {a} e {b} é {resul}'}

@app.post('/cidades', status_code=201)
def cidades_create(nova_cidade: NovaCidade):
    global atual_id
    atual_id +=1
    #o objeto cidade pega os atributos nome e uf do objeto nova_cidade da classe NovaCidade
    cidade = Cidade(id=atual_id, nome=nova_cidade.nome, uf=nova_cidade.uf)
    #teste: cidade=Cidade(id=atual_id,nome='barra',uf='pi')
    cidades.append(cidade)
    return cidade

@app.put('/cidades/{id}')
def alterar_cidade(id:int):
    for cidade in bancoc:
        if cidade.id==id:
            cidade.nome='nome alterado'
            cidade.uf='estado alterado'
            return {'ok': 'alterado'}
        else:
            return {'erro':'erro'}
@app.delete('/cidades/{id}')
def remover_cidade(id:int):
    for cidade in bancoc:
        if cidade.id==id:
            bancoc.pop(cidade)
            return {'ok': 'removido'}
        else:
            return {'erro':'erro'}


@app.get('/animais')
def listar_animais():
   return banco
@app.get('/animal/{animal_id}')
def obter_animal(animal_id:int):
    for animal in banco:
        if animal.id==animal_id:
            return animal
    return {'erro':'animal nao achado'}
@app.post('/animais')
def criar_animal(animal:Animal):
   animal.id=id+1
   banco.append(animal)
   return 'ok'
@app.delete('/animais/{animal_id}')
def remover_animal(animal_id:int):
    posicao=0
    for index,animal in enumerate(banco):
        if animal.id==animal_id:
            posicao=index
            break
    if posicao!=0:
       banco.pop(posicao)
       return {'ok': 'removido'}
    else:
       return {'erro':'erro'}
