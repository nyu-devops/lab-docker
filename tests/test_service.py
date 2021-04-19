# -*- coding: utf-8 -*-
# Copyright 2016, 2020 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Counter API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import patch
from flask_api import status  # HTTP Status Codes
from service import app, DATABASE_URI
from service.models import Counter

DATABASE_URI = os.getenv("DATABASE_URI", "redis://:@localhost:6379/0")

# logging.disable(logging.CRITICAL)

######################################################################
#  T E S T   C A S E S
######################################################################
class ServiceTest(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.testing = True
        app.debug = False

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        Counter.connect(DATABASE_URI)
        Counter.remove_all()
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ Get the home page """
        resp = self.app.get("/")
        self.assertEquals(resp.status_code, 200)

    def test_health(self):
        """ Get the health endpoint """
        resp = self.app.get("/health")
        self.assertEquals(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_counter(self):
        """ Create a counter """
        resp = self.app.post("/counters/foo")
        self.assertEquals(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["counter"], 0)

    def test_counter_already_exists(self):
        """ Counter already exists """
        resp = self.app.post("/counters/foo")
        self.assertEquals(resp.status_code, 201)
        resp = self.app.post("/counters/foo")
        self.assertEquals(resp.status_code, 409)

    def test_list_counters(self):
        """ Get the counter """
        resp = self.app.post("/counters/foo")
        self.assertEquals(resp.status_code, 201)
        resp = self.app.post("/counters/bar")
        self.assertEquals(resp.status_code, 201)
        resp = self.app.get("/counters")
        self.assertEquals(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_get_counter(self):
        """ Get the counter """
        self.test_create_counter()
        resp = self.app.get("/counters/foo")
        self.assertEquals(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["counter"], 0)

    def test_get_counter_not_found(self):
        """ Test counter not found """
        resp = self.app.get("/counters/foo")
        self.assertEquals(resp.status_code, 404)

    def test_put_counter_not_found(self):
        """ Test counter not found """
        resp = self.app.put("/counters/foo")
        self.assertEquals(resp.status_code, 404)

    def test_increment_counter(self):
        """ Increment the counter """
        self.test_get_counter()
        resp = self.app.put("/counters/foo")
        self.assertEquals(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["counter"], 1)

        resp = self.app.put("/counters/foo")
        self.assertEquals(resp.status_code, 200)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["counter"], 2)

    def test_delete_counter(self):
        """ Delete the counter """
        self.test_create_counter()
        resp = self.app.delete("/counters/foo")
        self.assertEquals(resp.status_code, 204)

    def test_method_not_allowed(self):
        """ Test Method Not Allowed """
        resp = self.app.post("/counters")
        self.assertEquals(resp.status_code, 405)


    ######################################################################
    #  T E S T   E R R O R   H A N D L E R S
    ######################################################################

    @patch("service.routes.Counter.find")
    def test_failed_get_request(self, value_mock):
        """ Error handlers for failed GET """
        value_mock.return_value = 0
        value_mock.side_effect = Exception()
        resp = self.app.get("/counters/foo")
        self.assertEqual(resp.status_code, 503)
    
    @patch("service.models.Counter.increment")
    def test_failed_update_request(self, value_mock):
        """ Error handlers for failed UPDATE """
        value_mock.return_value = 0
        value_mock.side_effect = Exception()
        self.test_create_counter()
        resp = self.app.put("/counters/foo")
        self.assertEqual(resp.status_code, 503)

    @patch("service.models.Counter.__init__")
    def test_failed_post_request(self, value_mock):
        """ Error handlers for failed POST """
        value_mock.return_value = 0
        value_mock.side_effect = Exception()
        resp = self.app.post("/counters/foo")
        self.assertEqual(resp.status_code, 503)

