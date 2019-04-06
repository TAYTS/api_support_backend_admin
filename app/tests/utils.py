from flask import jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies
)

# Import database models
from models.db import db
from models.users import Users


def get_cookie_from_response(response, cookie_name):
    """Extra the cookies from the response

    Arguments:
        response {Response} -- Response object
        cookie_name {String} -- Name of the cookie to extra

    Returns:
        dictionary -- Key-value pair of the cookie name and value
    """

    cookie_headers = response.headers.getlist('Set-Cookie')
    for header in cookie_headers:
        attributes = header.split(';')
        if cookie_name in attributes[0]:
            cookie = {}
            for attr in attributes:
                split = attr.split('=')
                cookie[split[0].strip().lower()] = split[1] if len(
                    split) > 1 else True
            return cookie
    return None


def fakeLogin(email, password):
    message = {"id_user_hash": ""}

    user = db.session.query(Users).filter(Users.email == email).first()
    if user:
        if user.check_password(password):
            access_token = create_access_token(
                identity=user.id_user_hash, fresh=True
            )
            refresh_token = create_refresh_token(
                identity=user.id_user_hash)

            access_expire = None
            refresh_expire = None

            message["id_user_hash"] = user.id_user_hash

            resp = make_response(jsonify(message), 200)

            set_access_cookies(resp, access_token, max_age=access_expire)
            set_refresh_cookies(resp, refresh_token,
                                max_age=refresh_expire)
            return resp
