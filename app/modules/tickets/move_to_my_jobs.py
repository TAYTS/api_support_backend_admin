from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords


@jwt_required
def move_to_my_jobs(postQuery):
    # Get the id_user_hash from the jwt_token

    id_user_hash = get_jwt_identity()

    # Get the id_user
    id_user = db.session.query(Users.id_user).filter(
        Users.id_user_hash == id_user_hash
    ).first()
    # Define return message
    message = {
        "status": 0
    }
    if id_user:
        # get ticket equal to postQuery
        ticket = db.session.query(TicketRecords).filter(
            TicketRecords.id_ticket_hash == postQuery
        ).first()
        try:
            # mark ticket as being assigned to admin
            ticket.status = 0
            # commit current user to be admin of problem
            ticket.id_admin = id_user.id_user
            db.session.commit()
            message["status"] = 1
            return jsonify(message), 200
        except Exception as e:
            current_app.logger.error("Unable to commit change to DB: " + str(e))
        return jsonify({"message": "Unable to commit change to DB."}), 500

    return jsonify({"message": "Invalid credential"}), 401
