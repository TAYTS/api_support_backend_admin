from flask import url_for
from app.tests.test_base import UserUnitTest
from uuid import uuid4
from datetime import datetime

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords


class TestRetrieveTicket(UserUnitTest):

    def populate_newjobs_ticket_record(self):
        id_user = db.session.query(Users.id_user).first()
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

    def test_retrieve_newjobs(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        self.populate_myjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="newjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 5
        )

    def test_retrieve_myjobs(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        self.populate_myjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="myjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 5
        )

    def test_retrieve_myjobs_invalid_userid(self):
        self.login_with_valid_credential()
        self.populate_newjobs_ticket_record()
        self.populate_myjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="myjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 0
        )
    # Current model does not account for difference in admin/user levels, thus all users can access newjobs
    # def test_retrieve_newjobs_invalid_userid(self):
    #     self.login_with_valid_credential()
    #     self.populate_newjobs_ticket_record()
    #     self.populate_myjobs_ticket_record()
    #     """ TESTING """
    #     response = self.client.get(
    #         url_for("tickets.retrieve_tickets", jobLevel="newjobs"),
    #         headers=self.csrf_headers
    #     )
    #
    #     resp_body = response.get_json()
    #     num_of_msg = len(resp_body)
    #     self.assert200(response)
    #     self.assertEqual(
    #         num_of_msg, 0
    #     )

    def test_retrieve_newjobs_without_token(self):
        self.populate_newjobs_ticket_record()
        self.populate_myjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="newjobs")
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {'msg': 'Missing cookie \"access_token_cookie\"'}
        )

    def test_retrieve_myjobs_without_token(self):
        self.populate_newjobs_ticket_record()
        self.populate_myjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="myjobs")
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {'msg': 'Missing cookie \"access_token_cookie\"'}
        )

    def test_retrieve_myjobs_empty(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="myjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 0
        )

    def test_retrieve_newjobs_empty(self):
        self.login_with_valid_credential_admin()
        self.populate_myjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="newjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 0
        )

    def test_retrieve_invalid_jobLevel(self):
        self.login_with_valid_credential_admin()
        self.populate_myjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel=str(uuid4())),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        self.assert404(response)
        self.assertEqual(
            resp_body[0], "Invalid URL."
        )
