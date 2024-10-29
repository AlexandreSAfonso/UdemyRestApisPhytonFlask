from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import check_password_hash
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json(), 200
        return {'message':'User Not Found.'}, 404 #not found

    def put(self, user_id):
        user = UserModel.find_user(user_id)
        dados = user.atributos.parse_args()
        user_finded = UserModel.find_user(user_id)
        if user_finded:
            user_finded.update_user(**dados)
            user_finded.save_user()
            return user_finded.json(), 200
        hotel = UserModel(**dados)
        try:
            hotel.save_user()
        except:
            return {'message': 'A Internal erro ocurred trying to save User'}, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, user_id):
        user_finded = UserModel.find_user(user_id)
        if user_finded:
            try:
                user_finded.delete_user()
            except:
                return {'message': 'A Internal erro ocurred trying to delete User'}, 500
            return {'message': 'User Deleted.'}, 200
        return {'message': 'User Not Found.'}, 404
        #return {'Hoteis': hoteis}

class UserRegister(Resource):
    # referent: /user_add
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
        atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")
        dados = atributos.parse_args()
        if UserModel.find_by_login(dados['login']):
            return{"message": "The login '{}' already existis.".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User Created successfully'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])
        if user and check_password_hash(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The Username or password is incorrect.'}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logget Out Successfully!'}, 200
