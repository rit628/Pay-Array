from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlalchemy as sql
import os
import re
from .auth import *
from xxhash import xxh32
import redis
from .orm import db, User, Item, user_preference
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

def create_app(name=__name__, testing=False):
    dupe_error_msg = re.compile(R"Duplicate entry \'([^\']*)\'")
    non_nullable_error_msg = re.compile(R"Column \'([^\']*)\' cannot be null")

    AUTH_TYPE = os.environ.get("AUTH_TYPE")
    API_VERSION = os.environ.get("API_VERSION")
    API_ROOT_PATH = f"/api/{API_VERSION}"

    CACHE_HOSTNAME = os.environ.get("CACHE_CONTAINER_NAME")
    CACHE_PORT = os.environ.get("CACHE_CONTAINER_PORT")
    CACHE_DB = 0 if not testing else 1

    RDBMS = "mysql"
    DRIVER = "mysqlconnector"
    DATABASE_HOSTNAME = os.environ.get("DATABASE_CONTAINER_NAME")
    USERNAME = os.environ.get("DATABASE_USER")
    PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD")
    DATABASE_PORT = os.environ.get("DATABASE_CONTAINER_PORT")
    DATABASE_PRODUCTION = os.environ.get('DATABASE_NAME_PRODUCTION')
    DATABASE_TEST = os.environ.get('DATABASE_NAME_TEST')

    PRODUCTION_URI = f"{RDBMS}+{DRIVER}://{USERNAME}:{PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_PRODUCTION}"
    TEST_URI = f"{RDBMS}+{DRIVER}://{USERNAME}:{PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_TEST}"

    app = Flask(name)
    CORS(app)
    cache = redis.Redis(host=CACHE_HOSTNAME, port=CACHE_PORT, db=CACHE_DB)
    app.config["SQLALCHEMY_DATABASE_URI"] = PRODUCTION_URI if not testing else TEST_URI
    db.init_app(app)        

    def get_auth_token() -> str:
        """Gets the JWT associated with the user requesting a resource.

        Raises:
            AuthenticationError: If token is missing or authorization header is invalid. Contains a 401 error code.

        Returns:
            str: User's JWT for authentication.
        """
        if request.authorization is None:
            raise AuthenticationError("Missing Token.")
        if request.authorization.type.capitalize() != AUTH_TYPE:
            raise AuthenticationError("Invalid Authorization Header.")
        return request.authorization.token

    def get_request_user() -> User:
        """Gets the user object associated with the request.

        Raises:
            NotFound: If a user with the provided id does not exist in the database. Contains a 404 error code.

        Returns:
            User: User object associated with id provided in authorization header.
        """
        token = get_auth_token()
        if cache.get(xxh32(token).hexdigest()) is not None:
            raise AuthenticationError("Invalid Token.")
        id = decode_token(token)["user_id"]
        user = db.get_or_404(User, id, description="User does not exist.")
        return user
    
    def get_item_by_name(name:str) -> Item:
        """Gets the item object with the given name.

        Args:
            name (str): Name of the item.

        Returns:
            Item: Item object with given name.
        """
        statement = sql.select(Item).where(Item.name == name)
        item = db.session.scalars(statement).first()
        if item is None:
            return jsonify(f"Item {name} not found."), 404
        return item

    @app.errorhandler(InvalidFieldError)
    def handle_invalid_field_error(error):
        response = jsonify(str(error))
        response.status_code = error.status_code
        return response

    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):
        response = jsonify(str(error))
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        error_msg = str(error.orig)
        dupe_error_match = dupe_error_msg.search(error_msg)
        non_nullable_error_match = non_nullable_error_msg.search(error_msg)
        if dupe_error_match:
            username = dupe_error_match.group(1)
            response = jsonify(f"{username} is already taken.")
        elif non_nullable_error_match:
            field = non_nullable_error_match.group(1)
            response = jsonify(f"User's {field} cannot be deleted.")
        else:
            response = jsonify(error_msg)
        response.status_code = 400
        return response
    
    @app.errorhandler(NotFound)
    def handle_notfound_error(error):
        response = jsonify(error.description)
        response.status_code = 404
        return response

    @app.route("/validate-server-runtime/", methods=["GET"])
    def validate_server_runtime():
        return jsonify("Hello World!"), 200

    @app.route("/validate-db-connection/", methods=["GET"])
    def validate_db_connection():
        tables = db.engine.connect().execute(sql.text("SHOW TABLES"))
        result = [tuple(i) for i in tables.fetchall()]
        return jsonify(result), 200

    @app.route(f"{API_ROOT_PATH}/login/", methods=["POST"])
    def login():
        supplied_credentials = request.get_json()
        username = supplied_credentials["username"]
        password = supplied_credentials["password"]
        statement = sql.select(User).where(User.username == username)
        user = db.session.scalars(statement).first()
        if user is None:    # guard if user is not found
            return jsonify(f"No Account with Username: {username}."), 404
        token = authenticate_user(user, password)
        response = f"{AUTH_TYPE} {token}"
        return jsonify(response), 201

    @app.route(f"{API_ROOT_PATH}/logout/", methods=["DELETE"])
    def logout():
        token = get_auth_token()
        exp_time = decode_token(token)["exp"]
        cache.set(xxh32(token).hexdigest(), 0, exat=exp_time)
        return jsonify("Logout Successful."), 200

    @app.route(f"{API_ROOT_PATH}/users/", methods=["POST"])
    def user_create():
        data = request.get_json()
        if "username" not in data:
            return jsonify("No Username Provided."), 400
        if "email" not in data:
            return jsonify("No Email Provided."), 400
        if "password" not in data:
            return jsonify("No Password Provided."), 400
        validate_user_data(data)
        
        password = data["password"]
        password_hash, salt = hash_password(password)
        data.update({
            "password_hash": password_hash,
            "salt": salt
        })
        data.pop("password")
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return jsonify("User Created Successfully."), 201
    
    @app.route(f"{API_ROOT_PATH}/users/me/", methods=["GET", "POST", "DELETE"])
    def user_access():
        user = get_request_user()
        if request.method == "GET":
            user_dict = user.to_dict()
            return jsonify(user_dict), 200
        elif request.method == "POST":
            data = request.get_json()
            if "password" in data:  # Password should be updated seperately
                data.pop("password")
            validate_user_data(data)
            for field, value in data.items():
                user.set_attr(field, value)
            db.session.commit()
            return jsonify("User Updated Successfully."), 200
        elif request.method == "DELETE":
            db.session.delete(user)
            db.session.commit()
            return jsonify("User Deleted Successfully."), 200
    
    @app.route(f"{API_ROOT_PATH}/users/me/preferences/", methods=["GET", "POST", "DELETE"])
    def user_preferences():
        user = get_request_user()
        if request.method == "GET":
            items = [item.to_dict() for item in user.items]
            return jsonify(items), 200
        elif request.method == "POST":
            data = request.get_json()
            item = Item(**data)
            user.items.append(item)
            db.session.commit()
            return jsonify(f"{item.name} added to {user.username}'s  preferences"), 200
        elif request.method == "DELETE":
            user.items.clear()
            db.session.commit()
            return jsonify(f"{user.username}'s item preferences cleared successfully."), 200
    
    @app.route(f"{API_ROOT_PATH}/users/me/preferences/<item>/", methods=["GET", "POST", "DELETE"])
    def user_preferences_item(item:str):
        user = get_request_user()
        if request.method == "GET":
            statement = sql.select(Item).where(Item.name == item).join(user_preference).join(User).where(User.id == user.id)           
            requested_item = db.session.scalars(statement).first()
            if requested_item is None:
                return jsonify(f"Item {item} not in {user.username}'s prefrences."), 404
            return jsonify(requested_item.to_dict()), 200
        elif request.method == "POST":
            retreived_item = get_item_by_name(item)
            user.items.append(retreived_item)
            db.session.commit()
            return f"{item.name} added to {user.username}'s  preferences", 200
        elif request.method == "DELETE":
            retreived_item = get_item_by_name(item)
            statement = user_preference.delete().where(user_preference.c.user_id == user.id).where(user_preference.c.item_id == retreived_item.id)
            db.session.execute(statement)
            db.session.commit()
            return jsonify(f"{user.username}'s item preference for {item} removed successfully."), 200
        
    
    @app.route(f"{API_ROOT_PATH}/users/me/<resource>/", methods=["GET", "POST", "DELETE"])
    def user_resource_access(resource:str):
        user = get_request_user()
        if request.method == "GET":
            fetched_resource = user.get_attr(resource)
            return jsonify(fetched_resource), 200
        elif request.method == "POST":
            data = request.get_json()
            validate_user_data({resource : data})
            if resource == "password":
                password_hash, salt = hash_password(data)
                setattr(user, "password_hash", password_hash)
                setattr(user, "salt", salt)
            else:
                user.set_attr(resource, data)
            db.session.commit()
            return jsonify(f"User's {resource} Updated Successfully."), 200
        elif request.method == "DELETE":
            user.set_attr(resource, None)
            db.session.commit()
            return jsonify(f"User's {resource} Deleted Successfully."), 200
        
    @app.route("/debug/", methods=["GET"])
    def debug():
        statement = sql.select(User)
        users = db.session.scalars(statement).all()
        users = [i.to_dict() for i in users]
        return users

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=os.environ.get("BACKEND_CONTAINER_PORT"))