# Importa a biblioteca 'json'.
import json


items = [
    {
        "id": 1,
        "name": "Bagulho",
        "description": "Apensas um bagulho",
        "location": "Em uma caixa"
    }, {
        "id": 2,
        "name": "Tranqueira",
        "descripton": "Apenas uma tranqueira qualquer",
        "location": "Em um gaveteriro"
    }, {
        "id": 3,
        "name": "Bagulhete",
        "description": "Um Bagulhete qualquer",
        "location": "na esquina"
    }


]
# Função que lê e lista todos os itens da coleção.
def get_all():
    
    # Converte a lista 'items' para json e armazena em 'var_json'
    # var_json=json.dumps(items, indent=2)
    
    return json.dumps(items, indent=2)
    
    #  Imprime o json.
    # print(var_json)
    
    # retorna json
    # return var_json

# Chama (call) a função get_all().    
# print(get_all())  

# Função que lê um item específico, identificado pelo índice.
def get_one(id):
    
    for item in items:
        if item.get("id") == id:
            return json.dumps(item, indent=2)

# Chama a função get_one(), passando o índice como parâmetro.
print(get_one(3))
    


# print(items[2]["location"])