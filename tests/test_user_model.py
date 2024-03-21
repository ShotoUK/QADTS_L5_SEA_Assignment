import unittest
from app import create_app, db
from app.models import User
from datetime import datetime

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User()
        self.user.Email = 'unittest@email.com'
        self.user.Password = 'testpassword'
        self.user.Role = 1
        self.user.FirstName = 'Test'
        self.user.LastName = 'User'
        self.user.DateCreated = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password_setter(self):
        u = User(password='testpassword')
        self.assertTrue(u.Password is not None)

    def test_no_password_getter(self):
        u = User(password = 'testpassword')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'testpassword')
        self.assertTrue(u.verify_password('testpassword'))
        self.assertFalse(u.verify_password('wrongpassword'))

    def test_password_salts_are_random(self):
        u = User(password = 'testpassword')
        u2 = User(password = 'testpassword')
        self.assertTrue(u.Password != u2.Password)
