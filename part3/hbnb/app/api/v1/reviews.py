from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace("reviews", description="Review operations")

review_create_model = api.model("ReviewCreate", {
    "text": fields.String(required=True, description="Review text"),
    "place_id": fields.String(required=True, description="Place ID"),
    "rating": fields.Integer(required=True, description="Rating (1-5)")
})

review_update_model = api.model("ReviewUpdate", {
    "text": fields.String(description="Review text"),
    "rating": fields.Integer(description="Rating (1-5)")
})


@api.route("/")
class Reviews(Resource):
    def get(self):
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

    @api.expect(review_create_model, validate=True)
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = api.payload or {}

        place_id = data.get("place_id")
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        # منع صاحب المكان يراجع مكانه
        if place.owner_id == current_user_id:
            api.abort(403, "You cannot review your own place")

        # منع التكرار (عندك method جاهزة)
        existing = facade.review_repo.get_by_user_and_place(current_user_id, place_id)
        if existing:
            api.abort(400, "Review already exists for this user and place")

        try:
            review = facade.create_review({
                "text": data["text"],
                "rating": data["rating"],
                "place_id": place_id,
                "user_id": current_user_id
            })
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:review_id>")
class ReviewResource(Resource):
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @api.expect(review_update_model, validate=True)
    @jwt_required()
    def put(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")

        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()

        if not is_admin and review.user_id != current_user_id:
            api.abort(403, "Forbidden")

        data = api.payload or {}

        if "text" in data and data["text"] is not None:
            review.text = data["text"]
        if "rating" in data and data["rating"] is not None:
            review.rating = data["rating"]

        facade.review_repo.update()
        return review.to_dict(), 200
