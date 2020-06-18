from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank"
        )
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every store needs a store id"
    )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"A store with name {name} already exists"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception as e:
            print(e)
            return {"message": "An error occured inserting the store"}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "store deleted"}


    def put(self, name):
        data = store.parser.parse_args()
        store = StoreModel.find_by_name(name)
        if not store:
            store = StoreModel(name, **data)
        else:
            store.price = data["price"]
        store.save_to_db()
        return store.json()


class StoreList(Resource):

    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
