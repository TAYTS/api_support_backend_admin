from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords
from app.config import EMAIL_SERVER_TOKEN, POSTMAN_TOKEN



@jwt_required
def email_user(postQuery):
    # Get the id_user_hash from the jwt_token

    id_user_hash = get_jwt_identity()

    # Get the id_user
    admin = db.session.query(Users).filter(
        Users.id_user_hash == id_user_hash
    ).first()
    # Define return message
    message = {
        "status": 0
    }
    if admin.is_admin == 1:
        # get ticket equal to postQuery
        ticket = db.session.query(TicketRecords).filter(
            TicketRecords.id_ticket_hash == postQuery
        ).first()
        # get email from original poster's userID
        user = db.session.query(Users).filter(
            Users.id_user == ticket.id_creator
        ).first()

        url = "https://ug-api.acnapiv3.io/swivel/email-services/api/mailer"
        subject = "Accenture support has replied to your ticket: " + postQuery
        email = user.email
        email = "kensim28@hotmail.com"
        body = "Your ticket: <b>" + postQuery + "</b> has recieved a reply. Please check the Accenture support portal at https://user.chocolatepie.tech/"
        payload = "{\n\t\"subject\": \"" + subject + "\",\n\t\"sender\": \"support@accenture.com\",\n\t\"recipient\": \"" + email + "\",\n\t\"html\": \"" + body + "\"\n}\n"
        headers = {
            'Server-Token': EMAIL_SERVER_TOKEN,
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': POSTMAN_TOKEN
        }
        # send post request to Accenture API
        response = requests.post("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            message["status"] = 1
            return jsonify(message), 200
        else:
            return jsonify({"message": "Error sending email"}), 500

    return jsonify({"message": "Invalid credential"}), 401
