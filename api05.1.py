# -*- coding: utf-8 -*-

import json
import sqlite3
import os


database = './db.db'




def get_all_items():
    try:
        
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        
        sql = "SELECT * FROM item WHERE item_status != 'off'"
        cursor.execute(sql)
        rows_data = cursor.fetchall()
        conn.close()

        
        list_data = []
        for row_data in rows_data:
            list_data.append(dict(row_data))

       
        if list_data:
            return list_data
        else:
            return {"error": "Nenhum item encontrado"}

    
    except sqlite3.Error as error:
        return {"error": f"Erro ao acessar o banco de dados: {str(error)}"}
    except Exception as error:
        return {"error": f"Erro inesperado: {str(error)}"}




def get_one_item(id):
    try:
        
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        
        sql = "SELECT * FROM item WHERE item_status != 'off' AND item_id = ?"
        cursor.execute(sql, (id,))
        row_data = cursor.fetchone()
        conn.close()

        
        if row_data:
            return dict(row_data)
        else:
            return {"error": "Item não encontrado"}
    
    
    except sqlite3.Error as error:
        return {"error": f"Erro ao acessar o banco de dados: {str(error)}"}
    except Exception as error:
        return {"error": f"Erro inesperado: {str(error)}"}



os.system('cls')


print(json.dumps(get_all_items(),ensure_ascii=False,indent=2))

print('\033[31;43m+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\033[m''\033[33;41m+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\033[m')

print(json.dumps(get_one_item(2),ensure_ascii=False,indent=2))
