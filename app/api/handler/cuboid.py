from http import HTTPStatus
from flask import Blueprint, jsonify, request
from app.api.model.bag import Bag
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
    width = content.get("width")
    height = content.get("height")
    depth = content.get("depth")
    bag_id = content.get("bag_id")

    bag = Bag.query.get(bag_id)
    if not bag:
        return {
                   "error": f"Bag with id #{bag_id} does not exist."
        }, HTTPStatus.NOT_FOUND


    cuboid_schema = CuboidSchema()
    cuboid = Cuboid(
        width=width,
        height=height,
        depth=depth,
        bag_id=bag_id,
    )
    db.session.add(cuboid)
    db.session.commit()

    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.CREATED


@cuboid_api.route("/<int:cuboid_id>", methods=["PUT"])
def update_cuboid(cuboid_id):
    content = request.json

    width = content.get("width")
    height = content.get("height")
    depth = content.get("depth")
    bag_id = content.get("bag_id")
    # todo: validate each attribute before updating them

    cuboid = Cuboid.query.get(cuboid_id)
    if not cuboid:
        return {
                   "error": f"Cuboid with id #{cuboid_id} does not exist."
        }, HTTPStatus.NOT_FOUND

    cuboid.width = width
    cuboid.height = height
    cuboid.depth = depth

    # Todo: break into isolated functions
    if bag_id:
        bag = Bag.query.get(bag_id)
        if not bag:
            return {
                       "error": f"Bag with id #{bag_id} does not exist."
            }, HTTPStatus.NOT_FOUND

        cuboid.bag_id = bag_id

    db.session.add(cuboid)
    db.session.commit()

    cuboid_schema = CuboidSchema()
    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.OK


@cuboid_api.route("/<int:cuboid_id>", methods=["DELETE"])
def delete_cuboid(cuboid_id):
    cuboid = Cuboid.query.get(cuboid_id)

    if not cuboid:
        return {
                   "error": f"Cuboid with id #{cuboid_id} does not exist."
        }, HTTPStatus.NOT_FOUND

    cuboid.query.delete()
    db.session.commit()
    return {}, HTTPStatus.OK
