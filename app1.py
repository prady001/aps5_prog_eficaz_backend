from bson import ObjectId, json_util
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from datetime import datetime
import json


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://gabrielprady1:lR6RItI2wEsXkTeY@cluster0.do8a1uo.mongodb.net/biblioteca_db"
mongo = PyMongo(app)

@app.route('/usuarios', methods=['GET'])
def get_all_users():
    # Define um filtro vazio para recuperar todos os usuários
    filtro = {}
    # Recupera os dados dos usuários do banco de dados MongoDB usando o filtro definido
    dados_usuarios = mongo.db.usuarios_aps5.find(filtro)
    
    # Convertendo os ObjectId para strings
    usuarios = []
    for user in dados_usuarios:
        user['_id'] = str(user['_id'])
        usuarios.append(user)

    # Cria uma resposta JSON contendo os usuários encontrados
    resp = {
        "usuarios": usuarios,
    }
    # Retorna a resposta JSON e o código de status 200 (OK)
    return json.dumps(resp), 200


@app.route('/usuarios/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    # Convert the user_id string to ObjectId
    try:
        user_id = ObjectId(user_id)
    except:
        # If the user_id is not a valid ObjectId, return a 400 Bad Request response
        return {'message': 'Invalid user ID'}, 400

    # Define a filter to retrieve the user by ID
    filtro = {'_id': user_id}

    # Retrieve the user data from the database
    user_data = mongo.db.usuarios_aps5.find_one(filtro)

    # If no user with the given ID is found, return a 404 Not Found response
    if not user_data:
        return {'message': 'User not found'}, 404

    # Convert the ObjectId to a string
    user_data['_id'] = str(user_data['_id'])

    # Return the user data as JSON with a 200 OK response
    return json.dumps(user_data), 200
    
@app.route('/usuarios', methods=['POST'])
def add_user():
    # Recupera os dados do novo usuário a partir do corpo da requisição
    novo_usuario = request.json
    # Insere os dados do novo usuário no banco de dados MongoDB
    resultado = mongo.db.usuarios_aps5.insert_one(novo_usuario)
    # Verifica se o novo usuário foi inserido com sucesso
    if resultado.inserted_id:
        # Cria uma resposta JSON contendo a mensagem de sucesso
        resp = {
            "mensagem": "Usuário adicionado com sucesso.",
        }
        # Retorna a resposta JSON e o código de status 201 (Created)
        return resp, 201
    else:
        # Cria uma resposta JSON contendo a mensagem de erro
        resp = {
            "erro": "Falha ao adicionar usuário.",
        }
        # Retorna a resposta JSON e o código de status 400 (Bad Request)
        return resp, 400
    

@app.route('/usuarios/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    # Convert the user_id string to ObjectId
    try:
        user_id = ObjectId(user_id)
    except:
        # If the user_id is not a valid ObjectId, return a 400 Bad Request response
        return {'message': 'Invalid user ID'}, 400

    # Get the updated user data from the request body
    updated_data = request.get_json()

    # Validate if the request body contains data
    if not updated_data:
        return {'message': 'No data provided for update'}, 400

    # Define a filter to find the user by ID
    filtro = {'_id': user_id}

    # Perform the update operation
    update_result = mongo.db.usuarios_aps5.update_one(filtro, {'$set': updated_data})

    # If no user is found with the given ID, return a 404 Not Found response
    if update_result.matched_count == 0:
        return {'message': 'User not found'}, 404

    # If the update operation is successful, return a success message with a 200 OK response
    return {'message': 'User updated successfully'}, 200



@app.route('/usuarios/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Convert the user_id string to ObjectId
    try:
        user_id = ObjectId(user_id)
    except:
        # If the user_id is not a valid ObjectId, return a 400 Bad Request response
        return {'message': 'Invalid user ID'}, 400

    # Define a filter to find the user by ID
    filtro = {'_id': user_id}

    # Perform the delete operation
    delete_result = mongo.db.usuarios_aps5.delete_one(filtro)

    # If no user is found with the given ID, return a 404 Not Found response
    if delete_result.deleted_count == 0:
        return {'message': 'User not found'}, 404

    # If the delete operation is successful, return a success message with a 200 OK response
    return {'message': 'User deleted successfully'}, 200

    
@app.route('/bikes', methods=['GET'])
def get_all_bikes():
    # Define um filtro vazio para recuperar todas as bikes
    filtro = {}
    # Recupera os dados dos usuários do banco de dados MongoDB usando o filtro definido
    dados_bikes = mongo.db.bikes_aps5.find(filtro)

    # Convertendo os ObjectId para strings
    bikes = []
    for bike in dados_bikes:
        bike['_id'] = str(bike['_id'])
        bikes.append(bike)

    # Cria uma resposta JSON contendo as bikes encontradas
    resp = {
        "bikes": bikes,
    }
    # Retorna a resposta JSON e o código de status 200 (OK)
    return json.dumps(resp), 200

@app.route('/bikes/<string:bike_id>', methods=['GET'])
def get_bike_by_id(bike_id):
    # Convert the bike_id string to ObjectId
    try:
        bike_id = ObjectId(bike_id)
    except:
        # If the bike_id is not a valid ObjectId, return a 400 Bad Request response
        return {'message': 'Invalid bike ID'}, 400

    # Define a filter to retrieve the bike by ID
    filtro = {'_id': bike_id}

    # Retrieve the bike data from the database
    bike_data = mongo.db.bikes_aps5.find_one(filtro)

    # If no bike with the given ID is found, return a 404 Not Found response
    if not bike_data:
        return {'message': 'Bike not found'}, 404

    # Convert the ObjectId to a string
    bike_data['_id'] = str(bike_data['_id'])

    # Return the bike data as JSON with a 200 OK response
    return json.dumps(bike_data), 200

@app.route('/bikes', methods=['POST'])
def add_bike():
    # Recupera os dados da nova bike a partir do corpo da requisição
    nova_bike = request.json
    # Insere os dados da nova bike no banco de dados MongoDB
    resultado = mongo.db.bikes_aps5.insert_one(nova_bike)
    # Verifica se a nova bike foi inserida com sucesso
    if resultado.inserted_id:
        # Cria uma resposta JSON contendo a mensagem de sucesso
        resp = {
            "mensagem": "Bike adicionada com sucesso.",
        }
        # Retorna a resposta JSON e o código de status 201 (Created)
        return resp, 201
    else:
        # Cria uma resposta JSON contendo a mensagem de erro
        resp = {
            "erro": "Falha ao adicionar bike.",
        }
        # Retorna a resposta JSON e o código de status 400 (Bad Request)
        return resp, 400
    
@app.route('/bikes/<string:bike_id>', methods=['PUT'])
def update_bike(bike_id):
    # Convert the bike_id string to ObjectId
    try:
        bike_id = ObjectId(bike_id)
    except:
        # If the bike_id is not a valid ObjectId, return a 400 Bad Request response
        return {'message': 'Invalid bike ID'}, 400

    # Get the updated bike data from the request body
    updated_data = request.get_json()

    # Validate if the request body contains data
    if not updated_data:
        return {'message': 'No data provided for update'}, 400

    # Define a filter to find the bike by ID
    filtro = {'_id': bike_id}

    # Perform the update operation
    update_result = mongo.db.bikes_aps5.update_one(filtro, {'$set': updated_data})

    # If no bike is found with the given ID, return a 404 Not Found response
    if update_result.matched_count == 0:
        return {'message': 'Bike not found'}, 404

    # If the update operation is successful, return a success message with a 200 OK response
    return {'message': 'Bike updated successfully'}, 200

@app.route('/bikes/<string:bike_id>', methods=['DELETE'])
def delete_bike(bike_id):
    # Convert the bike_id string to ObjectId
    try:
        bike_id = ObjectId(bike_id)
    except:
        # If the bike_id is not a valid ObjectId, return a 400 Bad Request response
        return {'message': 'Invalid bike ID'}, 400

    # Define a filter to find the bike by ID
    filtro = {'_id': bike_id}

    # Perform the delete operation
    delete_result = mongo.db.bikes_aps5.delete_one(filtro)

    # If no bike is found with the given ID, return a 404 Not Found response
    if delete_result.deleted_count == 0:
        return {'message': 'Bike not found'}, 404

    # If the delete operation is successful, return a success message with a 200 OK response
    return {'message': 'Bike deleted successfully'}, 200

@app.route('/emprestimos', methods=['POST'])
def registrar_emprestimo():
    dados_emprestimo = request.json
    bike_id = dados_emprestimo.get('bike_id')
    user_id = dados_emprestimo.get('user_id')

    bike = mongo.db.bikes_aps5.find_one({'_id': ObjectId(bike_id)})
    user = mongo.db.usuarios_aps5.find_one({'_id': ObjectId(user_id)})

    if not bike:
        return {'message': 'Bike not found'}, 404
    elif not user:
        return {'message': 'User not found'}, 404
    elif bike.get('emprestada'):
        return {'message': 'Bike already rented'}, 400

    dados_emprestimo['data_emprestimo'] = datetime.now()

    mongo.db.bikes_aps5.update_one({'_id': ObjectId(bike_id)}, {'$set': {'emprestada': True}})

    resultado = mongo.db.emprestimos_aps5.insert_one(dados_emprestimo)

    if resultado.inserted_id:
        return {'message': 'Loan registered successfully'}, 201
    else:
        return {'message': 'Failed to register loan'}, 400

@app.route('/emprestimos/usuario/<string:user_id>', methods=['GET'])
def emprestimos_por_usuario(user_id):
    emprestimos = list(mongo.db.emprestimos_aps5.find({'user_id': user_id}))
    return json_util.dumps(emprestimos), 200

@app.route('/emprestimos/bike/<string:bike_id>', methods=['GET'])
def emprestimos_por_bike(bike_id):
    emprestimos = list(mongo.db.emprestimos_aps5.find({'bike_id': bike_id}))
    return json_util.dumps(emprestimos), 200

@app.route('/emprestimos', methods=['GET'])
def listar_emprestimos():
    emprestimos = list(mongo.db.emprestimos_aps5.find())
    return json_util.dumps(emprestimos), 200

@app.route('/emprestimos/<string:emprestimo_id>', methods=['DELETE'])
def deletar_emprestimo(emprestimo_id):
    emprestimo = mongo.db.emprestimos_aps5.find_one({'_id': ObjectId(emprestimo_id)})
    if not emprestimo:
        return {'message': 'Loan not found'}, 404

    mongo.db.bikes_aps5.update_one({'_id': ObjectId(emprestimo['bike_id'])}, {'$set': {'emprestada': False}})
    mongo.db.emprestimos_aps5.delete_one({'_id': ObjectId(emprestimo_id)})

    return {'message': 'Loan deleted successfully'}, 200

@app.route('/emprestimos/<string:emprestimo_id>/devolucao', methods=['PUT'])
def marcar_devolucao(emprestimo_id):
    emprestimo = mongo.db.emprestimos_aps5.find_one({'_id': ObjectId(emprestimo_id)})
    if not emprestimo:
        return {'message': 'Loan not found'}, 404

    emprestimo['data_devolucao'] = datetime.now()

    mongo.db.bikes_aps5.update_one({'_id': ObjectId(emprestimo['bike_id'])}, {'$set': {'emprestada': False}})
    mongo.db.emprestimos_aps5.update_one({'_id': ObjectId(emprestimo_id)}, {'$set': {'data_devolucao': emprestimo['data_devolucao']}})

    return {'message': 'Loan marked as returned successfully'}, 200

if __name__ == '__main__':
    app.run(debug=True)