from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords
from datetime import datetime, date


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
        except:
            print("Commmit error")

        return jsonify(message), 200

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
