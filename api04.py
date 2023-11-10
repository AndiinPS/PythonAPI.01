
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


def get_all():  

   
    return json.dumps(items, indent=2)


def get_one(id): 

 
    try:
        id = int(id) 
        
        for item in items:  
        
            if item.get("id") == id:
               
             return json.dumps(item, indent=2)
       

    except:
       
        return False 
    
def new(json_date):
    print(json_date)
    return

def get_date():
 
    input_id = input("\033[34mDigite o ID do item: \033[m")

    view = get_one(input_id)

    if view:
        
        print(view)

    else:
        
        print("\033[31mAlgo errado não deu certo!\033[m")
        
def new(json_date):
   
    next_id = max(item["id"] for item in items) + 1
    print('\033[32mProxima ID\033[m' , next_id)
    return
    


my_json = '''
{ 
        "name": "Intercooler",
        "description": "Inox",
        "location": "Frontal"
    }
'''

new(my_json)



# get_date()  
# print(get_all())
# print(get_one())
# print(items[2]["location"])