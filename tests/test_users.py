# tests/test_users.py

import unittest
from flask import request
from flask_login import current_user
from base import BaseTestCase
from project import bcrypt
from project.models import User


class TestUser(BaseTestCase):

    # Ensure registration behaves correctly
    def test_correct_registration(self):
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(username="username", email="user@name.com",
                          password="password", confirm="password"),
                follow_redirects=True
            )
            self.assertIn(b'Click <a href="/logout">here</a> to logout.',
                          response.data)
            self.assertTrue(current_user.name == "username")
            self.assertTrue(current_user.is_active)
            user = User.query.filter_by(email="user@name.com").first()
            self.assertTrue(str(user) == '<name - username>')

    # Ensure correct errors are thrown on incorrect registration
    def test_incorrect_registration(self):
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(
                    username='fucker', email='fucker',
                    password='fucker', confirm='fucker'
                ),
                follow_redirects=True
            )
            self.assertIn(b'Invalid email address.', response.data)
            self.assertIn('/register', request.url)

    def test_get_by_id(self):
        #Ensure id is correct for the current logged in user
        with self.client:
            self.client.post('/login', data=dict(
                username="admin", password="admin"
            ), follow_redirects=True)
            self.assertTrue(current_user.id==1)
            self.assertFalse(current_user.id==20)

    def test_check_password(self):
        # Ensure that given password is correct after unhashing
        user = User.query.filter_by(email="ad@min.com").first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'pissass'))




if __name__ == '__main__':
    unittest.main()
