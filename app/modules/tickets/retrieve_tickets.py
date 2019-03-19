from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import database models
from models.db import db
from models.users import Users


@jwt_required
def retrieve_tickets():
    # Get the id_user_hash from the jwt_token
    id_user_hash = get_jwt_identity()

    # Get the id_user
    id_user = db.session.query(Users.id_user).filter(
        Users.id_user_hash == id_user_hash
    ).first()

    # Define the default return message
    messages = []

    messages.append({"sender": "bob",
                     "title": "hello there",
                     "body": "hello there this is the body"})

    messages.append({"sender": "mob",
                     "title": "hello theaaare",
                     "body": "hello thsdassdere this is the body"})

    return jsonify(messages), 200

    # Found the user
    # if id_user:
    #     # Get all the tickets and sort by the status
    #     tickets = db.session.query(TicketRecords).filter(
    #         TicketRecords.id_creator == id_user
    #     ).order_by(
    #         TicketRecords.id_ticket,
    #         TicketRecords.status
    #     ).all()
    #
    #     time_format = "%d %b %Y %I:%M %p"
    #     for ticket in tickets:
    #         base = {
    #             "title": ticket.title,
    #             "ticketID": ticket.id_ticket_hash,
    #             "create_timestamp": ticket.create_timestamp.strftime(time_format),
    #             "last_activity": ticket.last_activity_timestamp.strftime(time_format),
    #             "status": "Pending" if (ticket.status <= 0)else "Solved"
    #         }
    #         if ticket.status <= 0:
    #             messages["open"].append(base)
    #         else:
    #             messages["close"].append(base)
    #     return jsonify(messages), 200
    #
    # return jsonify({
    #     "message": "Invalid credential"
    # }), 401
