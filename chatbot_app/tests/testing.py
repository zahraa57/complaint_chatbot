# chatbot_app/tests/test_commands.py
from django.test import TestCase
from django.core.management import call_command
from chatbot_app.models import Customer, ChatMessage, Complaint
from unittest.mock import patch
from io import StringIO
import re


class ChatbotInteractionTest(TestCase):
    def test_chatbot_interaction(self):
        # Simulate user input
        input_data = "John Doe\n01065765351\njohn@example.com\n123 Main St\nhello\nexit\n"

        # Mock user input and capture command output
        with patch("builtins.input", side_effect=input_data.split("\n")), patch("sys.stdout", new_callable=StringIO) as output_buffer:
            call_command("chatbot_interaction")

            # Retrieve customer details from the database
            customer = Customer.objects.get(name="John Doe")
            self.assertEqual(customer.phone_number, "01065765351")
            self.assertEqual(customer.email, "john@example.com")
            self.assertEqual(customer.address, "123 Main St")

            # Retrieve chat messages from the database
            chat_messages = ChatMessage.objects.filter(customer=customer)
            self.assertTrue(chat_messages.exists())
            self.assertEqual(chat_messages.count(), 1)  

            # Retrieve complaint details from the database
            complaint = Complaint.objects.get(customer=customer)

            # Check if a unique ID is generated
            self.assertIsNotNone(complaint.unique_id)

            # Check if the loop exits when "exit" is entered
            with self.assertRaises(SystemExit):
                with patch("builtins.input", return_value="exit"):
                    call_command("chatbot_interaction")
