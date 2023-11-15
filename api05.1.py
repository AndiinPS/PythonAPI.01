# -*- coding: utf-8 -*-

import json
import sqlite3
import os

database = './db.db'

def get_one_owner(id):
    
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = "select * FROM owner WHERE owner_status !='off' AND owner_id=?"
    cursor.execute(sql, (id,))
    data = cursor.fetchone() 
    conn.close()
    
    if data:
        return dict(data) 
        
    else: 
        return {"ERRO": "Registro não encontrado."} 
 
 
os.system('cls')   
print (json.dumps(get_one_owner(5), ensure_ascii=False,indent=2))