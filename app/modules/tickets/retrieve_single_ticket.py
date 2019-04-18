from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import timedelta

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords

from app.utils.create_timestamp_str import create_timestamp_str


@jwt_required
def retrieve_single_ticket(jobLevel, postQuery):
    # Get the id_user_hash from the jwt_token

    id_user_hash = get_jwt_identity()

    # Get the id_user
    id_user = db.session.query(Users.id_user).filter(
        Users.id_user_hash == id_user_hash
    ).first()
    if id_user:
        # Define the default return message
        if jobLevel == "newjobs":
            ticket, creator_name = db.session.query(
                TicketRecords,
                Users.username
            ).join(
                Users,
                TicketRecords.id_creator == Users.id_user
            ).filter(
                TicketRecords.id_ticket_hash == postQuery,
                TicketRecords.id_admin == -1
            ).first()
        elif jobLevel == "myjobs":
            ticket, creator_name = db.session.query(
                TicketRecords,
                Users.username
            ).join(
                Users,
                TicketRecords.id_creator == Users.id_user
            ).filter(
                TicketRecords.id_ticket_hash == postQuery,
                TicketRecords.id_admin == id_user
            ).first()

        if ticket is None:
            return jsonify({"message": "Invalid ticket number"}), 404

        queryMessage = {
            "title": ticket.title,
            "sender": creator_name,
            "dateTime": create_timestamp_str(
                ticket.create_timestamp +
                timedelta(hours=8)
            ),
            "postID": ticket.id_ticket_hash,
            "category": ticket.category
        }
        return jsonify(queryMessage), 200
    return jsonify({
        "message": "Invalid credential"
    }), 401
