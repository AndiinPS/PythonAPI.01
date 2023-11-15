# -*- coding: utf-8 -*-

# Importa as bibliotecas de dependências para funcionar.

import json
import sqlite3
import os

database = './db.db' # Define banco de dados.

def get_all_items(): #Obtem todos os 'item' validos do banco de dados e retorna como uma 'list' de 'dict'.
    conn = sqlite3.connect(database) # Cria conexão com o banco de dados SQLite.
    conn.row_factory = sqlite3.Row # Define que a troca de dados e SQLite acontece em forma de row(Linhas).
    cursor = conn.cursor() # Aponta para a(s) linha(s) do SQLite.Row que sera acessado.
    sql = "select * FROM item WHERE item_status !='off'" # Query para consultar registros na tabela.
    cursor.execute(sql) # Executa o SQL acima no banco de dados.
    data = cursor.fetchall() # Cria variavel(armazena na memoria do computador) de dados do cursor para o Python.
    conn.close() # Desconecta Python do banco de dados.

    res = [] # Cria uma 'Lista'[] para armazenar as SQLite.Row na forma de 'dict'.

    for res_temp in data: # Loop que cada SQLite.Row da memoria(data).
        res.append(dict(res_temp)) # Converte a SQLite.Row(linha) item em dict(dicionario).

    return res # Devolve os dados processados.


def get_one_item(id):
    
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = "select * FROM item WHERE item_status !='off' AND item_id=?"
    cursor.execute(sql, (id,))
    data = cursor.fetchone() 
    conn.close()
    
    if data: # Se o registro existir.
        return dict(data) # Retorna o registro em 'dict'.
        
    else: # Se não existir. 
        return {"ERRO": "Registro não encontrado."} # Retorna 'erro' se não encontrar 
    
 
    
    
os.system('cls') # Limpa o console.

# print (json.dumps(get_all_items(), ensure_ascii=False,indent=2)) # json.dumps( exibe no console no formato Json) get_all_items(items obtidos da função) ensure_ascii=False(usando a tabela utf-8) indent=2(formata o Json).
print (json.dumps(get_one_item(7), ensure_ascii=False,indent=2)) # json.dumps( exibe no console no formato Json) get_one_item(item obtidos da função) ensure_ascii=False(usando a tabela utf-8) indent=2(formata o Json).
