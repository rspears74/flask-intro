# tests/test_basic.py

import unittest

from flask_login import current_user
from base import BaseTestCase

class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was setup correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    #Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn(b'Please login', response.data)


    # Ensure that posts show up on the main page
    def test_posts_show_up_on_main_page(self):
        response = self.client.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'This is a test', response.data)


class UsersViewsTests(BaseTestCase):

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            self.assertIn(b'You were logged in', response.data)
            self.assertTrue(current_user.name == "admin")
            self.assertTrue(current_user.is_active)


    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)


    # Ensure login behaves correctly with correct username, incorrect password
    def test_incorrect_login_password(self):
        response = self.client.post(
            '/login',
            data=dict(username="admin", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)


    # Ensure login behaves correctly with incorrect username, correct password
    def test_incorrect_login_username(self):
        response = self.client.post(
            '/login',
            data=dict(username="wrong", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)


    # Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out', response.data)
            self.assertFalse(current_user.is_active)


    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        response = self.client.get('/home', follow_redirects=True)
        self.assertIn(b'Please log in to access', response.data)


    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access', response.data)


if __name__ == '__main__':
    unittest.main()
