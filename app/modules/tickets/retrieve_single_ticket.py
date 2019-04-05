from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

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
        messages = []
        # Define the default return message
        if jobLevel == "newjobs":
            ticket = db.session.query(TicketRecords).filter(
                TicketRecords.id_ticket_hash == postQuery, TicketRecords.status == -1
            ).first()
        elif jobLevel=="myjobs":
            ticket = db.session.query(TicketRecords).filter(
                TicketRecords.id_ticket_hash == postQuery, TicketRecords.id_admin == id_user
            ).first()

        if ticket == None:
            return jsonify({"message": "Invalid ticket number"}), 205

        queryMessage = {
            "title": ticket.title,
            "sender": ticket.id_creator,
            "dateTime": create_timestamp_str(ticket.create_timestamp),
            "postID": ticket.id_ticket_hash
        }
        return jsonify(queryMessage), 200
    return jsonify({
        "message": "Invalid credential"
}), 401
