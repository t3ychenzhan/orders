"""
Item API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""

import unittest
import os
import json
import logging
from flask_api import status    # HTTP Status Codes
from mock import MagicMock, patch

from service.models.item import Item, DataValidationError
from service import db

import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestItemServer(unittest.TestCase):
    """ Item Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.app.debug = False
        app.initialize_logging(logging.INFO)
        # Set up the test database
        app.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        Item(product_id=1, name='hammer', quantity=1, price=11.50).save()
        Item(product_id=2, name='toilet paper', quantity=2, price=2.50).save()
        self.app = app.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_item(self):
        """ Create a new Item """
        item = {'product_id': 1, 'name': 'hammer', quantity: 1, price: 11.50}
        data = json.dumps(item)
        resp = self.app.post('/items', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'hammer')


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
