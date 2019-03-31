from flask import Blueprint

# Import all the view function
from app.modules.tickets.retrieve_tickets import retrieve_tickets
from app.modules.tickets.retrieve_single_ticket import retrieve_single_ticket
from app.modules.tickets.move_to_my_jobs import move_to_my_jobs

# Define the blueprint name
module = Blueprint("tickets", __name__)

module.add_url_rule("/tickets/retrieve-tickets/<jobLevel>",
                    view_func=retrieve_tickets, methods=["GET"])
module.add_url_rule("/tickets/retrieve-single-ticket/<jobLevel>/<postQuery>",
                    view_func=retrieve_single_ticket, methods=["GET"]),
module.add_url_rule("/tickets/move-to-my-jobs/<postQuery>",
                    view_func=move_to_my_jobs, methods=["GET"])
# get request, is params, which is in the link
