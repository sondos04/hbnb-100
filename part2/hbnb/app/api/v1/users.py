from flask_restx import Resource, Namespace, fields
from app.services.facade import facade

api = Namespace('users', description='User operations')

# ======================
# Models
# ======================

user_model = api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

# ======================
# Routes
# ======================

@api.route('/')
class Users(Resource):

    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        try:
            user = facade.create_user(api.payload)
            result = user.to_dict()
            result.pop("password", None)
            return result, 201
        except (TypeError, ValueError) as e:
            api.abort(400, str(e))

    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        result = []
        for user in users:
            data = user.to_dict()
            data.pop("password", None)
            result.append(data)
        return result, 200


@api.route('/<string:user_id>')
class User(Resource):

    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        result = user.to_dict()
        result.pop("password", None)
        return result, 200

    @api.expect(update_user_model)
    def put(self, user_id):
        """Update user"""
        data = api.payload or {}

        try:
            user = facade.update_user(user_id, data)
            if not user:
                api.abort(404, "User not found")

            result = user.to_dict()
            result.pop("password", None)
            return result, 200

        except (TypeError, ValueError) as e:
            api.abort(400, str(e))
