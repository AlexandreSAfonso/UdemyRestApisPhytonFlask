from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome':'Alha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome':'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id': 'chalie',
        'nome':'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Santa Catarina'
    }
]

class Hoteis(Resource):

    def get(self):
        return {'Hoteis': hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {'message':'Hotel Not Found.'}, 404 #not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 # Bad Request
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_finded = HotelModel.find_hotel(hotel_id)
        if hotel_finded:
            hotel_finded.update_hotel(**dados)
            hotel_finded.save_hotel()
            return hotel_finded.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel_finded = HotelModel.find_hotel(hotel_id)
        if hotel_finded:
            hotel_finded.delete_hotel()
            return {'message': 'Hotel Deleted.'}, 200
        return {'message': 'Hotel Not Found.'}, 404
        #return {'Hoteis': hoteis}
