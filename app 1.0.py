# -*- coding: utf-8 -*-


from flask import Flask, jsonify, request, abort, make_response, json, Response
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
CORS(app)


json.provider.DefaultJSONProvider.ensure_ascii = False

database = "./db.db"

def prefix_remove(prefix, data):

    new_data = {}
    for key, value in data.items():
        if key.startswith(prefix):
            new_key = key[len(prefix):]
            new_data[new_key] = value
        else:
            new_data[key] = value
    return new_data

@app.route("/items", methods=["GET"])
def get_all():

    # Obtém todos os registros válidos de 'item'.
    # Request method → GET
    # Request endpoint → /items
    # Response → JSON
    

    try:

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)

        # Formata os dados retornados na factory como SQLite.Row.
        conn.row_factory = sqlite3.Row

        # Cria um cursor de dados.
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM item WHERE item_status = 'on' ORDER BY item_date DESC")

        # Retorna todos os resultados da consulta para 'items_rows'.
        items_rows = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Cria uma lista para armazenar os registros.
        items = []

        # Converte cada SQLite.Row em um dicionário e adiciona à lista 'registros'.
        for item in items_rows:
            items.append(dict(item))

        # Verifica se há registros antes de retornar...
        if items:

            # Remove prefixos dos campos.
            new_items = [prefix_remove('item_', item) for item in items]

            # Se houver registros, retorna tudo.
            return new_items, 200
        else:
            # Se não houver registros, retorna erro.
            return {"error": "Nenhum item encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/items/<int:id>", methods=["GET"])
def get_one(id):

    # Obtém um registro único de 'item', identificado pelo 'id'.
    # Request method → GET
    # Request endpoint → /items/<id>
    # Response → JSON

    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM item WHERE item_id = ? AND item_status = 'on'", (id,))

        # Retorna o resultado da consulta para 'item_row'.
        item_row = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se o registro existe...
        if item_row:

            # Converte SQLite.Row para dicionário e armazena em 'item'.
            item = dict(item_row)

            # Remove prefixos dos campos.
            new_item = prefix_remove('item_', item)

            # Retorna item.
            return new_item, 200
        else:
            # Se não encontrar o registro, retorna erro.
            return {"error": "Item não encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route('/items', methods=["POST"])
def create():

    # Cadastra um novo registro em 'item'.
    # Request method → POST
    # Request endpoint → /items
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }}

    try:
        # Recebe dados do body da requisição na forma de 'dict'.
        new_item = request.get_json()

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que insere um novo registro na tabela 'item'.
        sql = "INSERT INTO item (item_name, item_description, item_location, item_owner) VALUES (?, ?, ?, ?)"

        # Dados a serem inseridos, obtidos do request.
        sql_data = (
            new_item['name'],
            new_item['description'],
            new_item['location'],
            new_item['owner']
        )

        # Executa a query, fazendo as devidas substituições dos curingas (?) pelos dados (sql_data).
        cursor.execute(sql, sql_data)

        # Obter o ID da última inserção
        inserted_id = int(cursor.lastrowid)

        # Salvar as alterações no banco de dados.
        conn.commit()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Retorna com mensagem de sucesso e status HTTP "201 Created".
        return {"success": "Registro criado com sucesso", "id": inserted_id}, 201

    except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/items/<int:id>", methods=["DELETE"])
def delete(id):

    # Marca, como apagado, um registro único de 'item', identificado pelo 'id'.
    # Request method → DELETE
    # Request endpoint → /items/<id>
    # Response → JSON → { "success": "Registro apagado com sucesso", "id": id do registro }

    try:

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que pesquisa a existência do registro.
        sql = "SELECT item_id FROM item WHERE item_id = ? AND item_status != 'off'"

        # Executa a query.
        cursor.execute(sql, (id,))

        # Retorna o resultado da consulta para 'item_row'.
        item_row = cursor.fetchone()

        # Se o registro exite e está ativo...
        if item_row:

            # Query para atualizar o item no banco de dados.
            sql = "UPDATE item SET item_status = 'off' WHERE item_id = ?"

            # Executa a query.
            cursor.execute(sql, (id,))

            # Salvar no banco de dados.
            conn.commit()

            # Fecha o banco de dados.
            conn.close()

            # Retorna com mensagem de sucesso e status HTTP "200 Ok".
            return {"success": "Registro apagado com sucesso", "id": id}, 200

        # Se o registro não existe, não pode ser apagado.
        else:

            # Fecha o banco de dados.
            conn.close()

            # Retorna mensagem de erro 404.
            return {"error": "Item não existe"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/items/<int:id>", methods=["PUT", "PATCH"])
def edit(id):

    # Edita um registro em 'item', identificado pelo 'id'.
    # Request method → PUT ou PATCH
    # Request endpoint → /items/<id>
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    #       OBS: usando "PATCH", não é necessário enviar todos os campos, apenas os que serão alterados.
    # Response → JSON → { "success": "Registro atualizado com sucesso", "id": id do registro }

    try:

        # Recebe os dados do corpo da requisição.
        item_json = request.get_json()

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Loop para atualizar os campos específicos do registro na tabela 'item'.
        # Observe que o prefixo 'item_' é adicionado ao(s) nome(s) do(s) campo(s).
        set_clause = ', '.join([f"item_{key} = ?" for key in item_json.keys()])

        # Monta SQL com base nos campos a serem atualizados.
        sql = f"UPDATE item SET {set_clause} WHERE item_id = ? AND item_status = 'on'"
        cursor.execute(sql, (*item_json.values(), id))

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        # Confirma a atualização.
        return {"success": "Registro atualizado com sucesso", "id": id}, 201

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/owners", methods=["GET"])
def get_all_owners():
    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)

        # Formata os dados retornados na factory como SQLite.Row.
        conn.row_factory = sqlite3.Row

        # Cria um cursor de dados.
        cursor = conn.cursor()

        # Executa o SQL para selecionar todos os proprietários em ordem alfabética.
        cursor.execute(
            "SELECT * FROM owner WHERE owner_status != 'off' ORDER BY owner_name COLLATE NOCASE ASC")

        # Retorna todos os resultados da consulta para 'owners_rows'.
        owners_rows = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Cria uma lista para armazenar os proprietários.
        owners = []

        # Converte cada SQLite.Row em um dicionário e adiciona à lista 'owners'.
        for owner in owners_rows:
            owners.append(dict(owner))

        # Verifica se há proprietários antes de retornar...
        if owners:
            # Remove prefixos dos campos.
            new_owners = [prefix_remove('owner_', owner) for owner in owners]

            # Se houver proprietários, retorna tudo.
            return new_owners, 200
        else:
            # Se não houver proprietários, retorna um erro.
            return {"error": "Nenhum proprietário encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/owners/<int:id>", methods=["GET"])
def get_one_owner(id):
    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL para selecionar um proprietário pelo ID.
        cursor.execute(
            "SELECT * FROM owner WHERE owner_id = ?", (id,))

        # Retorna o resultado da consulta para 'owner_row'.
        owner_row = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se o proprietário existe...
        if owner_row:
            # Converte SQLite.Row para dicionário e armazena em 'owner'.
            owner = dict(owner_row)

            # Remove prefixos dos campos.
            new_owner = prefix_remove('owner_', owner)

            # Retorna o proprietário.
            return new_owner, 200
        else:
            # Se não encontrar o proprietário, retorna erro.
            return {"error": "Proprietário não encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route('/owner', methods=["POST"])
def create_owner():
    try:
        # Recebe dados do body da requisição na forma de 'dict'.
        new_owner = request.get_json()

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que insere um novo registro na tabela 'owner'.
        sql = "INSERT INTO owner (owner_name, owner_email, owner_password, owner_birth) VALUES (?, ?, ?, ?)"

        # Dados a serem inseridos, obtidos do request.
        sql_data = (new_owner['name'], new_owner['email'], new_owner['password'], new_owner['birth'])

        # Executa a query, fazendo as devidas substituições dos curingas (?) pelos dados (sql_data).
        cursor.execute(sql, sql_data)

        # Obter o ID da última inserção
        inserted_id = int(cursor.lastrowid)

        # Salvar as alterações no banco de dados.
        conn.commit()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Retorna com mensagem de sucesso e status HTTP "201 Created".
        return {"success": "Proprietário cadastrado com sucesso", "id": inserted_id}, 201

    except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/owners/<int:id>", methods=["DELETE"])
def delete_owner(id):
    try:
        
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

       
        sql = "SELECT owner_id FROM owner WHERE owner_id = ? AND owner_status != 'off'"

       
        cursor.execute(sql, (id,))

        
        owner_row = cursor.fetchone()

        
        if owner_row:
            
            sql = "UPDATE owner SET owner_status = 'off' WHERE owner_id = ?"

            
            cursor.execute(sql, (id,))

            
            conn.commit()

            
            conn.close()

            
            return {"success": "Proprietário desativado com sucesso", "id": id}, 200

        
        else:
            
            conn.close()

            
            return {"error": "Proprietário não encontrado ou já está inativo"}, 404

    except sqlite3.Error as e:  
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/owners/<int:id>", methods=["PUT", "PATCH"])
def edit_owner(id):
    try:
        # Recebe os dados do corpo da requisição.
        owner_json = request.get_json()

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Loop para atualizar os campos específicos do registro na tabela 'owner'.
        set_clause = ', '.join([f"owner_{key} = ?" for key in owner_json.keys()])

        # Monta SQL com base nos campos a serem atualizados.
        sql = f"UPDATE owner SET {set_clause} WHERE owner_id = ?"
        cursor.execute(sql, (*owner_json.values(), id))

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        # Confirma a atualização.
        return {"success": "Registro de proprietário atualizado com sucesso", "id": id}, 201

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/owners/<int:id>/items", methods=["GET"])
def get_owner_items(id):
    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL para selecionar todos os itens do proprietário específico.
        cursor.execute(
            "SELECT * FROM item WHERE item_owner = ? AND item_status != 'off'", (id,))

        # Retorna todos os resultados da consulta para 'items_rows'.
        items_rows = cursor.fetchall()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Verifica se há itens antes de retornar...
        if items_rows:
            # Cria uma lista para armazenar os itens.
            items = []

            # Converte cada SQLite.Row em um dicionário e adiciona à lista 'items'.
            for item_row in items_rows:
                item = dict(item_row)
                # Remove prefixos dos campos.
                item = prefix_remove('item_', item)
                items.append(item)

            # Se houver itens, retorna tudo.
            return items, 200
        else:
            # Se não houver itens, retorna um erro.
            return {"error": "Nenhum item encontrado para este proprietário"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/item/<int:id>/owner", methods=["GET"])
def get_item_with_owner(id):
    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL para selecionar um item específico pelo ID, juntamente com seu proprietário.
        cursor.execute(
            "SELECT item.*, owner.* FROM item JOIN owner ON item.item_owner = owner.owner_id WHERE item.item_id = ? AND item.item_status != 'off'", (id,))

        # Obtém o resultado da consulta.
        item_owner_row = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se o item existir com o proprietário associado...
        if item_owner_row:
            # Cria um dicionário combinando os dados do item e do proprietário.
            item_with_owner = {
                "item": prefix_remove('item_', dict(item_owner_row)),
                "owner": prefix_remove('owner_', dict(item_owner_row))
            }

            # Retorna os detalhes do item com seu proprietário.
            return item_with_owner, 200
        else:
            # Se o item não existir ou não estiver associado a um proprietário ativo.
            return {"error": "Item não encontrado ou proprietário não está ativo"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/items/search/<string:query>")
def item_search(query):
    
    # Pesquisa todos os registros válidos de 'item' que conténha 'query' nos campos
    # 'item_name', 'item_description' ou 'item_location'.
    # Request method → GET
    # Request endpoint → /items/search/<string:query>
    # Response → JSON

    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = """
            SELECT * FROM item
            WHERE item_status != 'off' AND (
                item_name LIKE '%' || ? || '%' OR
                item_description LIKE '%' || ? || '%' OR
                item_location LIKE '%' || ? || '%'
            );        
        """
        cursor.execute(sql, (query, query, query))
        items_rows = cursor.fetchall()
        conn.close()

        items = []
        for item in items_rows:
            items.append(dict(item))

        if items:
            new_items = [prefix_remove('item_', item) for item in items]
            return new_items, 200
        else:
            return {"error": "Nenhum item encontrado"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500
    
    
@app.route("/contacts", methods=["POST"])
def contacts():

    # Cadastra um novo contato em 'contact'.
    # Request method → POST
    # Request endpoint → /contacts
    # Request body → JSON (raw) → { string:name, string:email, string:subject, string:message }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }

    try:
        new_item = request.get_json()
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        sql = "INSERT INTO contact (name, email, subject, message) VALUES (?, ?, ?, ?)"
        sql_data = (
            new_item['name'],
            new_item['email'],
            new_item['subject'],
            new_item['message']
        )
        cursor.execute(sql, sql_data)
        inserted_id = int(cursor.lastrowid)
        conn.commit()
        conn.close()

        if inserted_id > 0:
            return {"success": "Contato enviado com sucesso", "id": inserted_id, "name": new_item['name']}, 201

    except json.JSONDecodeError as e:
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500
    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500

# Roda aplicativo Flask.
if __name__ == "__main__":
    app.run(debug=True)
