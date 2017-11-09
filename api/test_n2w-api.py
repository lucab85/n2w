# test_n2w-api.py
import unittest
import os
import json
from app import create_app

class n2wapiTestCase(unittest.TestCase):
	"""This class represents the n2w-api Test Case"""

	def setUp(self):
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client
		self.app.app_context()

	def test_n2wapi_get_en(self):
		number = 11
		text = "eleven"
		lang = "en"
		url = '/n2w/api/v1.0/get/' + str(number) + "/" + lang
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		result_in_json = json.loads(rv.data.decode('utf-8'))
		self.assertEqual(number, result_in_json['number'])
		self.assertEqual(text, result_in_json['text'])
		self.assertEqual(lang, result_in_json['lang'])
		
		number = 121
		text = "one hundred and twenty-one"
		lang = "en"
		url = '/n2w/api/v1.0/get/' + str(number) + "/" + lang
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		result_in_json = json.loads(rv.data.decode('utf-8'))
		self.assertEqual(number, result_in_json['number'])
		self.assertEqual(text, result_in_json['text'])
		self.assertEqual(lang, result_in_json['lang'])

		number = 11.01
		text = "eleven point zero one"
		lang = "en"
		url = '/n2w/api/v1.0/get/' + str(number) + "/" + lang
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		result_in_json = json.loads(rv.data.decode('utf-8'))
		self.assertEqual(number, result_in_json['number'])
		self.assertEqual(text, result_in_json['text'])
		self.assertEqual(lang, result_in_json['lang'])

	def test_n2wapi_get_it(self):
		number = 11
		text = "undici"
		lang = "it"
		url = '/n2w/api/v1.0/get/' + str(number) + "/" + lang
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		result_in_json = json.loads(rv.data.decode('utf-8'))
		self.assertEqual(number, result_in_json['number'])
		self.assertEqual(text, result_in_json['text'])
		self.assertEqual(lang, result_in_json['lang'])

		number = 121
		text = "centoventiuno"
		lang = "it"
		url = '/n2w/api/v1.0/get/' + str(number) + "/" + lang
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		result_in_json = json.loads(rv.data.decode('utf-8'))
		self.assertEqual(number, result_in_json['number'])
		self.assertEqual(text, result_in_json['text'])
		self.assertEqual(lang, result_in_json['lang'])
		
		number = 11.01
		text = "undici virgola zero uno"
		lang = "it"
		url = '/n2w/api/v1.0/get/' + str(number) + "/" + lang
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		result_in_json = json.loads(rv.data.decode('utf-8'))
		self.assertEqual(number, result_in_json['number'])
		self.assertEqual(text, result_in_json['text'])
		self.assertEqual(lang, result_in_json['lang'])

	def test_n2wapi_langs(self):
		url = '/n2w/api/v1.0/langs'
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		result_in_json = json.loads(rv.data.decode('utf-8'))
		self.assertIsInstance(result_in_json['langs'], list)

	def test_n2wapi_get_400(self):
		number = 11
		lang = "XX"
		url = '/n2w/api/v1.0/get/' + str(number) + "/" + lang
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 400)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')

	def test_n2wapi_get_404(self):
		url = '/n2w/'
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 404)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		url = '/n2w/api/'
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 404)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		url = '/n2w/api/v1.0/'
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 404)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')
		url = '/n2w/api/v1.0/get/'
		rv = self.client().get(url)
		self.assertEqual(rv.status_code, 404)
		self.assertEqual(rv.content_type, "application/json")
		self.assertEqual(rv.headers['Access-Control-Allow-Origin'], '*')

	def tearDown(self):
	  """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()
