import unittest
from app import create_app, db
from app.models import Role
from datetime import datetime

class RoleTestCase(unittest.TestCase):
    def setUp(self):
        # Create a new app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a new database
        db.create_all()

        # Create a new role
        self.role = Role()
        self.role.Name = 'Test Role'
        self.role.Permissions = 1

        # Add the role to the database
        db.session.add(self.role)
        db.session.commit()

        # Get database Role
        self.dbRole = Role.query.filter_by(Name='Test Role').first()

    def tearDown(self):
        # Remove the role from the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_role_exists(self):
        self.assertTrue(self.dbRole is not None)

    def test_role_name(self):
        self.assertEqual(self.dbRole.Name, 'Test Role')

    def test_role_permissions(self):
        self.assertEqual(self.dbRole.Permissions, 1)