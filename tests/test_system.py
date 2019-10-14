from __future__ import unicode_literals, absolute_import

import os
import sys
import unittest

from flaskblog import app

class TestResponse(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def test_web_response404(self):
        result = self.app.get('/') 
        self.assertEqual(result.status_code, 404) 

    def test_web_response405(self):
        result = self.app.get('/callback') 
        self.assertEqual(result.status_code, 405) 
    
if __name__ == "__main__":
    unittest.main()