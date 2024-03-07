import unittest
from app.models import Customer

class DeleteCustomerTestCase(unittest.TestCase):
    def setUp(self):
        self.customer = Customer()
        self.customer.Name = 'Test Customer'
        self.customer.Status = 'Active'
        self.customer.AgentId = 1
        self.customer.ProductId = 1
        self.customer.Description = 'Description'
        self.customer.ContactName = 'Company Contact'
        self.customer.ContactEmail = 'test@testmail.com'
        self.customer.ContactPhone = '01204123654'
        self.customer.DateCreated = '2018-01-01 00:00:00'
        self.customer.notes = ''

    def test_customer_exists(self):
        self.assertTrue(self.customer is not None)

