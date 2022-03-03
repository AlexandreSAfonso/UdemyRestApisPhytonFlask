from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {'Hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'Nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
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
        try:
            hotel.save_hotel()
        except:
            return {'message': 'A Internal erro ocurred trying to save Hotel'}, 500
        return hotel.json(), 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_finded = HotelModel.find_hotel(hotel_id)
        if hotel_finded:
            hotel_finded.update_hotel(**dados)
            hotel_finded.save_hotel()
            return hotel_finded.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'A Internal erro ocurred trying to save Hotel'}, 500
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel_finded = HotelModel.find_hotel(hotel_id)
        if hotel_finded:
            try:
                hotel_finded.delete_hotel()
            except:
                return {'message': 'A Internal erro ocurred trying to delete Hotel'}, 500
            return {'message': 'Hotel Deleted.'}, 200
        return {'message': 'Hotel Not Found.'}, 404
        #return {'Hoteis': hoteis}
