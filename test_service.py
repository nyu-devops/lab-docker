# -*- coding: utf-8 -*-

# run with:
# python -m unittest discover

import unittest
import json
import service

class TestServer(unittest.TestCase):

    def setUp(self):
        service.app.debug = True
        self.app = service.app.test_client()
        service.init_redis('127.0.0.1', 6379, None)

    def test_index(self):
        resp = self.app.get('/')
        self.assertTrue ('Hit Counter Docker Application' in resp.data)
        self.assertEquals(resp.status_code, 200)

    def test_get_counter(self):
        resp = self.app.get('/counter')
        self.assertEquals(resp.status_code, 200)
        parsed_json = json.loads(resp.data)
        self.assertTrue (parsed_json['counter'] is not None)

    def test_increment_counter(self):
        # get the current counter and increment it
        resp = self.app.get('/counter')
        self.assertEquals(resp.status_code, 200)
        parsed_json = json.loads(resp.data)
        count = int(parsed_json['counter'])

        # post and make sure the counter is increments
        resp = self.app.get('/counter')
        self.assertEquals(resp.status_code, 200)
        resp = self.app.get('/counter')
        self.assertEquals(resp.status_code, 200)

        # check that it was incremented by 2
        parsed_json = json.loads(resp.data)
        new_count = int(parsed_json['counter'])
        self.assertTrue (count + 2 == new_count)

    def test_reset_counter(self):
        # get the current counter and increment it 3 times
        resp = self.app.get('/counter')
        resp = self.app.get('/counter')
        resp = self.app.get('/counter')
        self.assertEquals(resp.status_code, 200)
        # now reset the counter to zero
        resp = self.app.post('/counter')
        self.assertEquals(resp.status_code, 201)
        parsed_json = json.loads(resp.data)
        count = int(parsed_json['counter'])
        self.assertEquals(count, 0)


if __name__ == '__main__':
    unittest.main()
