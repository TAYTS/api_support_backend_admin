from flask import url_for
from app.tests.test_base import UserUnitTest
from uuid import uuid4
from datetime import datetime

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords


class TestMoveToMyJobs(UserUnitTest):

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

    def add_single_newjobs_ticket_record(self, id_ticket_hash):
        id_user = db.session.query(Users.id_user).order_by(
            Users.create_timestamp
        ).first()
        title = "testing"
        category = "testing"
        # Create 5 ticket records
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
        return ticket

    def test_move_ticket_with_incorrect_id_ticket(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        """ TESTING """
        response = self.client.get(
            url_for("tickets.move_to_my_jobs", postQuery=str(uuid4())),
            headers=self.csrf_headers
        )
        self.assert500(response)
        self.assertEqual(
            response.get_json(),
            {"message": "Unable to commit change to DB."}
        )

    def test_move_ticket_with_known_id_ticket(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        self.add_single_newjobs_ticket_record(id_ticket_hash)
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

        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="newjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 11
        )

        response = self.client.get(
            url_for("tickets.move_to_my_jobs", postQuery=id_ticket_hash),
            headers=self.csrf_headers
        )
        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {"status": 1}
        )

        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="myjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 1
        )

        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="newjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 10
        )

    def test_move_multiple_tickets_with_known_id_ticket(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        id_ticket_hash1 = str(uuid4())
        self.add_single_newjobs_ticket_record(id_ticket_hash1)
        id_ticket_hash2 = str(uuid4())
        self.add_single_newjobs_ticket_record(id_ticket_hash2)
        id_ticket_hash3 = str(uuid4())
        self.add_single_newjobs_ticket_record(id_ticket_hash3)
        id_ticket_hash4 = str(uuid4())
        self.add_single_newjobs_ticket_record(id_ticket_hash4)
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

        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="newjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 14
        )

        response = self.client.get(
            url_for("tickets.move_to_my_jobs", postQuery=id_ticket_hash1),
            headers=self.csrf_headers
        )
        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {"status": 1}
        )

        response = self.client.get(
            url_for("tickets.move_to_my_jobs", postQuery=id_ticket_hash2),
            headers=self.csrf_headers
        )
        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {"status": 1}
        )
        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="myjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 2
        )

        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="newjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 12
        )
        response = self.client.get(
            url_for("tickets.move_to_my_jobs", postQuery=id_ticket_hash3),
            headers=self.csrf_headers
        )
        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {"status": 1}
        )

        response = self.client.get(
            url_for("tickets.move_to_my_jobs", postQuery=id_ticket_hash4),
            headers=self.csrf_headers
        )
        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {"status": 1}
        )

        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="myjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 4
        )

        response = self.client.get(
            url_for("tickets.retrieve_tickets", jobLevel="newjobs"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        num_of_msg = len(resp_body)
        self.assert200(response)
        self.assertEqual(
            num_of_msg, 10
        )

    def test_move_ticket_without_token(self):
        self.populate_newjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        self.add_single_newjobs_ticket_record(id_ticket_hash)
        """ TESTING """
        response = self.client.get(
            url_for("tickets.move_to_my_jobs", postQuery=id_ticket_hash)
        )
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {'msg': 'Missing cookie \"access_token_cookie\"'}
        )

    def test_move_ticket_without_csrf_token(self):
        self.login_with_valid_credential_admin()
        self.populate_newjobs_ticket_record()
        id_ticket_hash = str(uuid4())
        self.add_single_newjobs_ticket_record(id_ticket_hash)
        """ TESTING """
        response = self.client.get(
            url_for("tickets.move_to_my_jobs", postQuery=id_ticket_hash)
        )
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {'msg': 'Missing CSRF token in headers'}
        )
