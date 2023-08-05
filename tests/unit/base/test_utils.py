import os
from django.core import mail
from django.test import TestCase
from base.utils import get_url_from_hostname, EmailService, get_file_content
from django.conf import settings


class TestGetUrl(TestCase):
    def test_get_url_from_hostname(self):
        settings.DEBUG = True
        url = get_url_from_hostname("localhost:8000")
        self.assertEqual(url, "http://localhost:8000")

    def test_get_url_from_hostname_with_https(self):
        settings.DEBUG = False
        settings.TEST = False
        url = get_url_from_hostname("localhost:8000")
        self.assertEqual(url, "https://localhost:8000")

class TestEmailService(TestCase):
    def test_email_service(self):
        subject = "Test Email"
        message = "This is a test email."
        recipient_list = ["test@example.com"]
        from_email = "noreply@example.com"
        html_message = "<p>This is a <strong>test</strong> email.</p>"

        EmailService(subject, message, recipient_list, from_email, html_message)

        # Check that the email was sent successfully
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].body, message)
        self.assertEqual(mail.outbox[0].from_email, from_email)
        self.assertEqual(mail.outbox[0].to, recipient_list)
        self.assertEqual(mail.outbox[0].alternatives[0][0], html_message)


class TestGetFileContent(TestCase):
    def setUp(self):
        # Create a temporary file with sample content for testing
        self.file_path = "test_file.txt"
        with open(self.file_path, "w") as f:
            f.write("This is a test file.\nLine 2.\nLine 3.")

    def tearDown(self):
        # Remove the temporary file after the test is done
        os.remove(self.file_path)

    def test_get_file_content_existing_file(self):
        # Test when providing an existing file path
        expected_content = "This is a test file.\nLine 2.\nLine 3."
        actual_content = get_file_content(self.file_path, "r")
        self.assertEqual(actual_content, expected_content)

    def test_get_file_content_nonexistent_file(self):
        # Test when providing a non-existent file path
        nonexistent_file = "nonexistent.txt"
        with self.assertRaises(FileNotFoundError):
            get_file_content(nonexistent_file, "r")
