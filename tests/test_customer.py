import unittest
from app import create_app, db
from app.models import Customer
from datetime import datetime

class CustomerTestCase(unittest.TestCase):
    def setUp(self):
        # Create a new customer
        self.customer = Customer()
        self.customer.Name = 'Test Customer'
        self.customer.Status = 'Active'
        self.customer.AgentId = 1
        self.customer.ProductId = 1
        self.customer.Description = 'Description'
        self.customer.ContactName = 'Company Contact'
        self.customer.ContactEmail = 'test@testmail.com'
        self.customer.ContactPhone = '01204123654'
        self.customer.DateCreated = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

        # Create a new app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a new database
        db.create_all()

        # Add the customer to the database
        db.session.add(self.customer)
        db.session.commit()

        # Get database Customer
        self.dbCustomer = Customer.query.filter_by(Name='Test Customer').first()

    def tearDown(self):
        # Remove the customer from the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_customer_exists(self):
        self.assertTrue(self.dbCustomer is not None)

    def test_customer_name(self):
        self.assertEqual(self.dbCustomer.Name, 'Test Customer')

    def test_customer_status(self):
        self.assertEqual(self.dbCustomer.Status, 'Active')

    def test_customer_agent(self):
        self.assertEqual(self.dbCustomer.AgentId, 1)

    def test_customer_product(self):
        self.assertEqual(self.dbCustomer.ProductId, 1)

    def test_customer_description(self):
        self.assertEqual(self.dbCustomer.Description, 'Description')

    def test_customer_contactname(self):
        self.assertEqual(self.dbCustomer.ContactName, 'Company Contact')

    def test_customer_contactemail(self):
        self.assertEqual(self.dbCustomer.ContactEmail, 'test@testmail.com')

    def test_customer_contactphone(self):
        self.assertEqual(self.dbCustomer.ContactPhone, '01204123654')

    def test_customer_datecreated(self):
        self.assertEqual(self.dbCustomer.DateCreated, datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))

    def test_delete_customer(self):
        db.session.delete(self.dbCustomer)
        db.session.commit()
        self.assertTrue(Customer.query.filter_by(Name='Test Customer').first() is None)



