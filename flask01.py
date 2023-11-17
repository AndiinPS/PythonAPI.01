# -*- coding: utf-8 -*-

# Bibliotecas usadas:

from flask import Flask, jsonify, request, abort, make_response, json, Response

app=Flask(__name__) #Cria aplicativo Flask

json.provider.DefaultJSONProvider.ensure_ascii=False # Configura character set das transações HTTP para UTF-8

database="./db.db" # Banco de dados SQLite

# Obtem todos os registros validos de 'item', request mrthod - GET , resquest endpoint ,  response - Json

@app.route("/items", methods=["GET"])
def get_all():
    return {"Hello":"Word"}
    
if __name__=="__main__": #Roda o app Flask
    app.run(debug=True)
    
    