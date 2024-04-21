from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId, json_util
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://gabrielprady1:lR6RItI2wEsXkTeY@cluster0.do8a1uo.mongodb.net/biblioteca_db"
mongo = PyMongo(app)

@app.route('/usuarios', methods=['GET'])
def get_all_users():
    usuarios = list(mongo.db.usuarios_aps5.find({}, {'_id': 0}))
    return jsonify(usuarios), 200

@app.route('/usuarios/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = mongo.db.usuarios_aps5.find_one({'_id': ObjectId(user_id)}, {'_id': 0})
    if user:
        return jsonify(user), 200
    else:
        return {'message': 'User not found'}, 404

@app.route('/usuarios', methods=['POST'])
def add_user():
    novo_usuario = request.json
    resultado = mongo.db.usuarios_aps5.insert_one(novo_usuario)
    if resultado.inserted_id:
        return {'message': 'User added successfully'}, 201
    else:
        return {'message': 'Failed to add user'}, 400

@app.route('/usuarios/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    filtro = {'_id': ObjectId(user_id)}
    dados_atualizados = request.json
    resultado = mongo.db.usuarios_aps5.update_one(filtro, {'$set': dados_atualizados})
    if resultado.modified_count:
        return {'message': 'User updated successfully'}, 200
    else:
        return {'message': 'User not found'}, 404

@app.route('/usuarios/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    filtro = {'_id': ObjectId(user_id)}
    resultado = mongo.db.usuarios_aps5.delete_one(filtro)
    if resultado.deleted_count:
        return {'message': 'User deleted successfully'}, 200
    else:
        return {'message': 'User not found'}, 404

@app.route('/bikes', methods=['GET'])
def get_all_bikes():
    bikes = list(mongo.db.bikes_aps5.find({}, {'_id': 0}))
    return jsonify(bikes), 200

@app.route('/bikes/<string:bike_id>', methods=['GET'])
def get_bike_by_id(bike_id):
    bike = mongo.db.bikes_aps5.find_one({'_id': ObjectId(bike_id)}, {'_id': 0})
    if bike:
        return jsonify(bike), 200
    else:
        return {'message': 'Bike not found'}, 404

@app.route('/bikes', methods=['POST'])
def add_bike():
    nova_bike = request.json
    resultado = mongo.db.bikes_aps5.insert_one(nova_bike)
    if resultado.inserted_id:
        return {'message': 'Bike added successfully'}, 201
    else:
        return {'message': 'Failed to add bike'}, 400

@app.route('/bikes/<string:bike_id>', methods=['PUT'])
def update_bike(bike_id):
    filtro = {'_id': ObjectId(bike_id)}
    dados_atualizados = request.json
    resultado = mongo.db.bikes_aps5.update_one(filtro, {'$set': dados_atualizados})
    if resultado.modified_count:
        return {'message': 'Bike updated successfully'}, 200
    else:
        return {'message': 'Bike not found'}, 404

@app.route('/bikes/<string:bike_id>', methods=['DELETE'])
def delete_bike(bike_id):
    filtro = {'_id': ObjectId(bike_id)}
    resultado = mongo.db.bikes_aps5.delete_one(filtro)
    if resultado.deleted_count:
        return {'message': 'Bike deleted successfully'}, 200
    else:
        return {'message': 'Bike not found'}, 404

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
