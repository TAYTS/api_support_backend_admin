from flask import url_for
from app.tests.test_base import UserUnitTest
from uuid import uuid4
from datetime import datetime

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords


class TestSingleTicket(UserUnitTest):

    def populate_newjobs_ticket_record(self):
        id_user = db.session.query(Users.id_user).order_by(
            Users.create_timestamp
        ).first()
        title = "testing"
        category = "testing"
        # Create 5 ticket records
        for i in range(5):
            id_ticket_hash = str(uuid4())
            timestamp = datetime.utcnow().replace(microsecond=0)

            ticket = TicketRecords(
                id_ticket_hash=id_ticket_hash,
                id_creator=id_user,
                id_channel=str(uuid4()),
                title=title,
                status=-1,
                category=category,
                create_timestamp=timestamp,
                last_activity_timestamp=timestamp
            )
            db.session.add(ticket)
            db.session.commit()

    def populate_myjobs_ticket_record(self):
        ids = db.session.query(Users.id_user).order_by(
            Users.create_timestamp
        ).all()
        id_user = ids[0]
        id_admin = ids[1]
        title = "testing"
        category = "testing"
        # Create 5 ticket records
        for i in range(5):
            id_ticket_hash = str(uuid4())
            timestamp = datetime.utcnow().replace(microsecond=0)
            ticket = TicketRecords(
                id_ticket_hash=id_ticket_hash,
                id_creator=id_user,
                id_channel=str(uuid4()),
                title=title,
                status=0,
                id_admin=id_admin,
                category=category,
                create_timestamp=timestamp,
                last_activity_timestamp=timestamp
            )
            db.session.add(ticket)
            db.session.commit()

    def add_single_newjobs_ticket_record(self, id_ticket_hash, timestamp=datetime.utcnow().replace(microsecond=0)):
        id_user = db.session.query(Users.id_user).order_by(
            Users.create_timestamp
        ).first()
        title = "testing"
        category = "testing"
        # Create 5 ticket records

        ticket = TicketRecords(
            id_ticket_hash=id_ticket_hash,
            id_creator=id_user,
            id_channel=str(uuid4()),
            title=title,
            status=-1,
            category=category,
            create_timestamp=timestamp,
            last_activity_timestamp=timestamp
        )

        db.session.add(ticket)
        db.session.commit()
        return ticket

    def add_single_myjobs_ticket_record(self, id_ticket_hash, timestamp=datetime.utcnow().replace(microsecond=0)):
        ids = db.session.query(Users.id_user).order_by(
            Users.create_timestamp
        ).all()
        id_user = ids[0]
        id_admin = ids[1]
        title = "testing"
        category = "testing"
        # Create 5 ticket records

        ticket = TicketRecords(
            id_ticket_hash=id_ticket_hash,
            id_creator=id_user,
            id_channel=str(uuid4()),
            title=title,
            status=0,
            id_admin=id_admin,
            category=category,
            create_timestamp=timestamp,
            last_activity_timestamp=timestamp
        )

        db.session.add(ticket)
        db.session.commit()
        return ticket

    def test_retrieve_single_newjobs(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        timestamp = datetime.utcnow().replace(microsecond=0)
        self.add_single_newjobs_ticket_record(id_ticket_hash, timestamp)
        self.populate_newjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_single_ticket", jobLevel="newjobs", postQuery=id_ticket_hash),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        userID = db.session.query(Users.id_user).order_by(
            Users.create_timestamp
        ).first()
        timestampString = timestamp.strftime("%d %b %Y %I:%M %p")
        self.assert200(response)
        self.assertEqual(
            resp_body, {
                "title": "testing",
                "sender": userID[0],
                "dateTime": timestampString,
                "postID": id_ticket_hash
            }
        )

    def test_retrieve_single_myjobs(self):
        self.login_with_valid_credential_admin()
        self.populate_myjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        timestamp = datetime.utcnow().replace(microsecond=0)
        self.add_single_myjobs_ticket_record(id_ticket_hash, timestamp)
        self.populate_myjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_single_ticket", jobLevel="myjobs", postQuery=id_ticket_hash),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        userID = db.session.query(Users.id_user).order_by(
            Users.create_timestamp
        ).first()
        timestampString = timestamp.strftime("%d %b %Y %I:%M %p")
        self.assert200(response)
        self.assertEqual(
            resp_body, {
                "title": "testing",
                "sender": userID[0],
                "dateTime": timestampString,
                "postID": id_ticket_hash
            }
        )

    def test_retrieve_single_newjobs_incorrect_id_ticket(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        timestamp = datetime.utcnow().replace(microsecond=0)
        self.add_single_newjobs_ticket_record(id_ticket_hash, timestamp)
        self.populate_newjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_single_ticket", jobLevel="newjobs", postQuery=str(uuid4())),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        userID = db.session.query(Users.id_user).order_by(
            Users.create_timestamp
        ).first()
        self.assertEqual(
            resp_body, {"message": "Invalid ticket number"}
        )

    def test_retrieve_single_myjobs_incorrect_id_ticket(self):
        self.login_with_valid_credential_admin()
        self.populate_myjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        timestamp = datetime.utcnow().replace(microsecond=0)
        self.add_single_myjobs_ticket_record(id_ticket_hash, timestamp)
        self.populate_myjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_single_ticket", jobLevel="myjobs", postQuery=str(uuid4())),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        userID = db.session.query(Users.id_user).order_by(
            Users.create_timestamp
        ).first()
        self.assertEqual(
            resp_body, {"message": "Invalid ticket number"}
        )

    def test_retrieve_single_myjobs_without_token(self):
        self.populate_myjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        self.add_single_myjobs_ticket_record(id_ticket_hash)
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_single_ticket", jobLevel="myjobs", postQuery=id_ticket_hash
                    ))
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {'msg': 'Missing cookie \"access_token_cookie\"'}
        )

    def test_retrieve_single_myjobs_without_csrf_token(self):
        self.login_with_valid_credential_admin()
        self.populate_myjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        self.add_single_myjobs_ticket_record(id_ticket_hash)
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_single_ticket", jobLevel="myjobs", postQuery=id_ticket_hash
                    ))
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {'msg': 'Missing CSRF token in headers'}
        )

    def test_retrieve_single_newjobs_without_token(self):
        self.populate_newjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        self.add_single_newjobs_ticket_record(id_ticket_hash)
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_single_ticket", jobLevel="newjobs", postQuery=id_ticket_hash
                    ))
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {'msg': 'Missing cookie \"access_token_cookie\"'}
        )

    def test_retrieve_single_newjobs_without_csrf_token(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        self.add_single_newjobs_ticket_record(id_ticket_hash)
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_single_ticket", jobLevel="newjobs", postQuery=id_ticket_hash
                    ))
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {'msg': 'Missing CSRF token in headers'}
        )
