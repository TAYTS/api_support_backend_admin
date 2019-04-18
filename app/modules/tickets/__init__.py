from flask import Blueprint

# Import all the view function
from app.modules.tickets.retrieve_tickets import retrieve_tickets
from app.modules.tickets.retrieve_single_ticket import retrieve_single_ticket
from app.modules.tickets.move_to_my_jobs import move_to_my_jobs
from app.modules.tickets.create_ticket import create_ticket
from app.modules.tickets.retrieve_user_tickets import retrieve_user_tickets
from app.modules.tickets.email_user import email_user
from app.modules.tickets.resolve_ticket import resolve_ticket

# Define the blueprint name
module = Blueprint("tickets", __name__)

module.add_url_rule("/tickets/retrieve-tickets/<jobLevel>",
                    view_func=retrieve_tickets, methods=["GET"])
module.add_url_rule("/tickets/retrieve-single-ticket/<jobLevel>/<postQuery>",
                    view_func=retrieve_single_ticket, methods=["GET"]),
module.add_url_rule("/tickets/move-to-my-jobs/<postQuery>",
                    view_func=move_to_my_jobs, methods=["GET"])
module.add_url_rule("/tickets/create-tickets",
                    view_func=create_ticket, methods=["POST"])
module.add_url_rule("/tickets/retrieve-user-tickets",
                    view_func=retrieve_user_tickets, methods=["GET"])
module.add_url_rule("/tickets/email-user/<postQuery>",
                    view_func=email_user, methods=["GET"])
module.add_url_rule("/tickets/resolve-ticket",
                    view_func=resolve_ticket, methods=["PUT"])
