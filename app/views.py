from flask.globals import request
from app.models import User
from flask_restplus import Resource
from app.dto import UserDto


user_api = UserDto.api
_user = UserDto.user


@user_api.route("/")
class UserCollection(Resource):
    @user_api.doc(description="Add user to database")
    @user_api.response(201, "User successfully created.")
    @user_api.marshal_with(_user)
    @user_api.expect(_user)
    def post(self):
        return User.create_user(request.json), 201

    @user_api.doc(description="Get all users from database")
    @user_api.marshal_list_with(_user)
    def get(self):
        return User.get_all_users()


@user_api.route("/<int:user_id>")
class UserItem(Resource):
    @user_api.doc(description="Get user by id from database")
    @user_api.marshal_with(_user)
    def get(self, user_id):
        return User.get_user(user_id)

    @user_api.response(204, "User successfully deleted.")
    @user_api.doc(description="Delete user from database")
    def delete(self, user_id):
        User.delete_user(user_id)
        return "", 204
