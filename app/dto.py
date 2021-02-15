from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace("user", description="user related operations")
    user = api.model(
        "user",
        {
            "id": fields.Integer(description="user id"),
            "firstname": fields.String(required=True, description="user firstname"),
            "lastname": fields.String(required=True, description="user lastname"),
            "gender": fields.String(required=True, description="user gender"),
            "email": fields.String(required=True, description="user email"),
            "phone": fields.String(required=True, description="user phone"),
        },
    )
