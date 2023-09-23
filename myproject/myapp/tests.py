# my_extension/tests.py
from django.test import TestCase
import io  # Import the io module
from rest_framework.test import APIClient
from .models import Greeting
import logging  # Import the logging module for capturing logs

class GreetingTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_submit_greeting(self):
        # Test submitting a greeting
        response = self.client.post('/api/greetings/', {'greeting': 'hello'}, format='json')
        self.assertEqual(response.status_code, 201)  # Assuming your view returns a 201 status on success

        # Check if the greeting is saved in the database
        greeting = Greeting.objects.first()
        self.assertEqual(greeting.text, 'hello')
        self.assertIsNotNone(greeting.created_at)

        # Test submitting a different greeting
        response = self.client.post('/api/greetings/', {'greeting': 'goodbye'}, format='json')
        self.assertEqual(response.status_code, 201)

        # Ensure that the "hello" greeting results in a recursive call to the API
        # You can check this by capturing logs
        logs = self.captured_logs.getvalue()  # Captured logs from the test

        # Assert that the log message indicating the recursive call is present
        self.assertIn("Making a recursive call with greeting: goodbye", logs)

    def setUp(self):
        # Initialize the logger to capture logs
        self.captured_logs = logging.getLogger("my_extension")
        self.captured_logs.setLevel(logging.INFO)  # Adjust the log level as needed
        self.log_capture_string = io.StringIO()
        ch = logging.StreamHandler(self.log_capture_string)
        self.captured_logs.addHandler(ch)

    def tearDown(self):
        # Clean up and remove the log handler
        self.captured_logs.removeHandler(self.log_capture_string)
