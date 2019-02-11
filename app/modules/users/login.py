from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies

# Import database models
from models.db import db
from models.user import Users


def login():
    # Get the data from the request JSON
    username = str(request.json.get("username"))
    password = str(request.json.get("password"))

    # Check if the data is present
    if username and password:
        user = db.session.query(
            Users
        ).filter(
            Users.email == username
        ).first()
        if user:
            if user.check_password(password):
                access_token = create_access_token(identity=user.id_user_hash)
                resp = jsonify({"login": True})
                set_access_cookies(resp, access_token)
                return resp, 200
        else:
            return jsonify({
                "Message": "User Not Found"
            }), 404
    else:
        # Return error message if the data is incomplete
        return jsonify({
            "Message": "Missing information"
        }), 400
