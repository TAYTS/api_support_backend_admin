from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import database models
from models.db import db
from models.users import Users
from datetime import datetime, date
from models.tickets import TicketRecords

from app.utils.create_timestamp_str import create_timestamp_str



@jwt_required
def retrieve_tickets(jobLevel):
    # Get the id_user_hash from the jwt_token
    id_user_hash = get_jwt_identity()

    # Get the id_user
    id_user = db.session.query(Users.id_user).filter(
        Users.id_user_hash == id_user_hash
    ).first()
    messages = []
    # Define the default return message
    # if (jobLevel == "newjobs"):
    # Found the user
    if id_user:
        if jobLevel == "newjobs":
            # Get all the tickets and sort by the status
            tickets = db.session.query(TicketRecords).filter(
                TicketRecords.status == -1
            ).order_by(
                TicketRecords.last_activity_timestamp
            ).all()
            for ticket in tickets:
                base = {
                    "title": ticket.title,
                    "ticketID": ticket.id_ticket_hash,
                    "create_timestamp": create_timestamp_str(ticket.create_timestamp),
                    "last_activity": create_timestamp_str(ticket.last_activity_timestamp)
                }
                messages.append(base)
        elif jobLevel == "myjobs":
            None
            # Get all the tickets and sort by the status
            # print(id_user)
            # tickets = db.session.query(TicketRecords).filter(
            #     TicketRecords.status == -1
            # ).order_by(
            #     TicketRecords.last_activity_timestamp
            # #     ,desc()??
            # ).all()
            # print(tickets)
            # for ticket in tickets:
            #     base = {
            #         "title": ticket.title,
            #         "ticketID": ticket.id_ticket_hash,
            #         "create_timestamp": create_timestamp_str(ticket.create_timestamp),
            #         "last_activity": create_timestamp_str(ticket.last_activity_timestamp)
            #     }
            #     messages.append(base)
        return jsonify(messages), 200

    return jsonify({
        "message": "Invalid credential"
    }), 401

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
