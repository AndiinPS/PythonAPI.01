# Importa a biblioteca 'json'.
import json


items = [
    {
        "id": 1,
        "name": "Ecu",
        "description": "Injeção programavél",
        "location": "Painel interno"
    }, {
        "id": 2,
        "name": "Bicos",
        "description": "Injetores",
        "location": "Coletor plenum"
    }, {
        "id": 3,
        "name": "Cabeçote",
        "description": "Preparado",
        "location": "Bloco do motor"
    }, {
        "id": 4,
        "name": "Pistão",
        "description": "Forjado",
        "location": "Bloco do motor"
    }, {
        "id": 5,
        "name": "Turbo",
        "description": "Turbina",
        "location": "Coletor de escape"
    }, {
        "id": 6,
        "name": "Escapamento",
        "description": "Inox",
        "location": "Full inox"

    }, {
        "id": 7,
        "name": "Biela",
        "description": "Forjada",
        "location": "Bloco do motor"

    }, {
        "id": 8,
        "name": "Embreagem",
        "description": "Cerâmica",
        "location": "Volante motor"
    }
]
# Função que lê e lista todos os itens da coleção.
def get_all():
    
    # Converte a lista 'items' para json e armazena em 'var_json'
    var_json=json.dumps(items, indent=2)
    
     # Imprime o json.
    print(var_json)

# Chama (call) a função get_all().    
get_all()  

# Função que lê um item específico, identificado pelo índice.
def get_one(id):
    
     # Converte o dicionario 'items[id]' para json e armazena em 'var_json'
    var_json=json.dumps(items[id], indent=2) 
     
     # Imprime o json.
    print(var_json)

# Chama a função get_one(), passando o índice como parâmetro.
get_one(0)    
    


# print(items[2]["location"])