
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

def get_all():
    var_json=json.dumps(items, indent=2)
    print(var_json)
    
# get_all()  

def get_one(id):
    var_json=json.dumps(items[id], indent=2)  
    print(var_json)

get_one(0)    
    


# print(items[2]["location"])