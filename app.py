from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
#app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=14) // 14 dias
api = Api(app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self,token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401

#api.add_resource(/, 'pageland')
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hotel/<string:hotel_id>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/user_add')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
# to Authorization use  Bearer token
