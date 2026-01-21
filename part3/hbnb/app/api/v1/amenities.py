from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

# API Models

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

update_amenity_model = api.model('AmenityUpdate', {
    'name': fields.String(description='Name of the amenity')
})

# Amenity List

@api.route('/')
class AmenityList(Resource):

    def get(self):
        """Public: Get all amenities"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

    @api.expect(amenity_model, validate=True)
    @jwt_required()
    def post(self):
        """Admin only: Create amenity"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        amenity = facade.create_amenity(api.payload)
        return amenity.to_dict(), 201

# Amenity Resource

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):

    def get(self, amenity_id):
        """Public: Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.to_dict(), 200

    @api.expect(update_amenity_model, validate=True)
    @jwt_required()
    def put(self, amenity_id):
        """Admin only: Update amenity"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        amenity = facade.update_amenity(amenity_id, api.payload)
        if not amenity:
            api.abort(404, "Amenity not found")

        return amenity.to_dict(), 200
