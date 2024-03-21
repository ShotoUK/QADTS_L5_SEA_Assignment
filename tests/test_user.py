import unittest
from app import create_app, db
from app.models import User
from datetime import datetime

class UserTestCase(unittest.TestCase):
    def setUp(self):
        # Create a new app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a new database
        db.create_all()

        # Create a new user
        self.user = User()
        self.user.Email = 'unittest@email.com'
        self.user.Password = 'testpassword'
        self.user.Role = 1
        self.user.FirstName = 'Test'
        self.user.LastName = 'User'
        self.user.DateCreated = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        
        # Add the user to the database
        db.session.add(self.user)
        db.session.commit()

        # Get database User
        self.dbUser = User.query.filter_by(Email=self.user.Email).first()

    def tearDown(self):
        # Remove the user from the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_exists(self):
        self.assertTrue(self.dbUser is not None)

    def test_user_email(self):
        self.assertEqual(self.dbUser.Email, 'unittest@email.com')

    def test_user_password(self):
        self.assertTrue(self.dbUser.Password, self.user.Password)

    def test_user_role(self):
        self.assertEqual(self.dbUser.Role, 1)

    def test_user_firstname(self):
        self.assertEqual(self.dbUser.FirstName, 'Test')

    def test_user_lastname(self):
        self.assertEqual(self.dbUser.LastName, 'User')

    def test_user_datecreated(self):
        self.assertEqual(self.dbUser.DateCreated, datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))

    