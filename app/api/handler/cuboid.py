from http import HTTPStatus
from flask import Blueprint, jsonify, request
from app.api.model.cuboid import Cuboid
from app.api.schema.cuboid import CuboidSchema
from app.api.db import db

cuboid_api = Blueprint("cuboid_api", __name__)


@cuboid_api.route("/", methods=["GET"])
def list_cuboids():
    cuboid_ids = request.args.getlist("cuboid_id")
    cuboid_schema = CuboidSchema(many=True)
    cuboids = Cuboid.query.filter(Cuboid.id.in_(cuboid_ids)).all()

    return jsonify(cuboid_schema.dump(cuboids)), HTTPStatus.OK


@cuboid_api.route("/<int:cuboid_id>", methods=["GET"])
def get_cuboid(cuboid_id):
    cuboid = Cuboid.query.get(cuboid_id)

    if not cuboid:
        return {
                   "error": f"Cuboid with id #{cuboid_id} does not exist."
        }, HTTPStatus.NOT_FOUND

    volume = cuboid.depth * cuboid.width * cuboid.height

    response = {
        "depth": cuboid.depth,
        "height": cuboid.height,
        "id": cuboid.id,
        "width": cuboid.width,
        "volume": volume
    }
    return response, HTTPStatus.OK


@cuboid_api.route("/", methods=["POST"])
def create_cuboid():
    content = request.json

    cuboid_schema = CuboidSchema()
    cuboid = Cuboid(
        width=content["width"],
        height=content["height"],
        depth=content["depth"],
        bag_id=content["bag_id"],
    )
    db.session.add(cuboid)
    db.session.commit()

    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.CREATED
