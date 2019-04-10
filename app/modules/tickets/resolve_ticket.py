from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords


@jwt_required
def resolve_ticket():
    # Get all the parametes
    id_ticket_hash = str(request.json.get("id_ticket_hash"))

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
        ticket = db.session.query(TicketRecords).filter(
            TicketRecords.id_ticket_hash == id_ticket_hash
        ).first()

        if ticket:
            ticket.status = 1
            db.session.commit()

        message["status"] = 1
        return jsonify(message), 200
    else:
        return jsonify(message), 401

    return jsonify(message), 500
