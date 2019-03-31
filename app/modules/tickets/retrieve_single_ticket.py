from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import database models
from models.db import db
from models.users import Users
from datetime import datetime, date


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
        if (jobLevel == "newjobs"):
            test1time = date(2019, 3, 22)

            postID = 0

            messages.append({"postID": postID,
                             "sender": "aaaa",
                             "title": "hellcvsvdvo tdsdasdhere",
                             "body": "hello thedsvdsvsdqre czxcxthis is the body",
                             "dateTime": test1time})
            postID += 1
            messages.append({"postID": postID, "sender": "mob",
                             "title": "hello t2123123123heaaare",
                             "body": "hello 1221e taacassccssachis is the body",
                             "dateTime": test1time})

            test1time = date(2019, 3, 21)
            postID += 1
            messages.append({"postID": postID, "sender": "aaaa",
                             "title": "hello tdsdasdhere",
                             "body": "hello there czxcxthis is the body",
                             "dateTime": test1time})
            postID += 1
            messages.append({"postID": postID, "sender": "mob",
                             "title": "hello theaaare",
                             "body": "hello thsdazxczxcssdere taacassccssachis is the body",
                             "dateTime": test1time})

            test1time = date(2019, 3, 15)
            postID += 1
            messages.append({"postID": postID, "sender": "bob",
                             "title": "hello there",
                             "body": "hello there this is the body",
                             "dateTime": test1time})
            postID = 20
            messages.append({"postID": postID, "sender": "mob",
                             "title": "hello theaaare",
                             "body": "hello thsdassdere this is the body",
                             "dateTime": test1time})

        elif (jobLevel == "myjobs"):
            test1time = date(2019, 3, 22)

            postID = 0

            messages.append({"postID": postID,
                             "sender": "bbbbb",
                             "title": "asdasddad tdsdasdhere",
                             "body": "loremsandosadoasdodasposadaopspcmoczx",
                             "dateTime": test1time})
            postID += 1
            messages.append({"postID": postID, "sender": "moasdsadb",
                             "title": "hello asd2ddsadasds",
                             "body": "hello 12asdd22dasdasdasd21e taacassccssachis is the body",
                             "dateTime": test1time})

            test1time = date(2019, 3, 21)
            postID += 1
            messages.append({"postID": postID, "sender": "aa2ddsdwdwdaa",
                             "title": "helsadad12d12d2lo tdsdaassdhere",
                             "body": "hesadadq2d2dwqllo there czxcxthis is the body",
                             "dateTime": test1time})
            postID += 1
            messages.append({"postID": postID, "sender": "moqwdwqd2qd21db",
                             "title": "heqddwqdqwdllo theaaare",
                             "body": "wqdqdwqdwdqwdqwdhello thsdazxczxcssdere taacassccssachis is the body",
                             "dateTime": test1time})

            test1time = date(2019, 3, 15)
            postID += 1
            messages.append({"postID": postID, "sender": "bob",
                             "title": "helqwdqwdqwdwqdwqlo there",
                             "body": "hello there this is the body",
                             "dateTime": test1time})
            postID = 20
            messages.append({"postID": postID, "sender": "mob",
                             "title": "hello theaaare",
                             "body": "hello thsdassdere this is the body",
                             "dateTime": test1time})


        # todo fix error reporting here
        # for message in messages:
        #     print(int(message["postID"]) == int(postQuery))
        #     if int(message["postID"]) == int(postQuery):
        #         queryMessage  = message
        #         break
        queryMessage = {"postID": 123, "sender": "mob",
                             "title": "hello theaaare",
                             "body": "hello thsdassdere this is the body",
                             "dateTime":  date(2019, 3, 22)}
        return jsonify(queryMessage), 200
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
