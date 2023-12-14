# chatbot_app/management/commands/chatbot_interaction.py
import argparse
import uuid
from django.core.management.base import BaseCommand
from transformers import T5ForConditionalGeneration, T5Tokenizer

from chatbot_app.models import Customer, ChatMessage, Complaint

class Command(BaseCommand):
    help = 'Interact with customers using a chatbot'

    def handle(self, *args, **options):
        # Collect customer information
        name = input("Enter your name: ")
        phone_number = input("Enter your phone number:")
        email = input("Enter your email address: ")
        address = input("Enter your physical address: ")
        # Save customer details to the database
        customer = Customer.objects.create(name=name, phone_number=phone_number, email=email, address=address)
        # Trigger model validation
        
        ## add try except to handel the error 
        customer.full_clean()

        customer.save()

        # Initialize the T5 transformer
        #tokenizer = T5Tokenizer.from_pretrained('google/flan-t5-xl')
        #model = T5ForConditionalGeneration.from_pretrained('google/flan-t5-xl')

        # Start the conversation
        #conversation = f"Customer: {name}, Phone: {phone_number}, Email: {email}, Address: {address}\n"

        # while True:
        #     user_input = input("You: ")
        #     if user_input.lower() == 'exit':
        #         break

        #     # Incorporate the user input into the conversation
        #     #conversation += f"User: {user_input}\n"

        #     # Generate a response using exit T5 transformer
        #     inputs = tokenizer.encode(user_input, return_tensors='pt', max_length=512, truncation=True)
        #     response = model.generate(inputs, max_length=100)
        #     chatbot_response = tokenizer.decode(response[0], skip_special_tokens=True)
        #     print(f"Chatbot: {chatbot_response}")

        #     # Log the chat message
        #     #ChatMessage.objects.create(customer=customer, message=user_input)

        # # Generate a summary of the customer's problem
        # complaint_summary = " ".join([message.message for message in customer.chatmessage_set.all()])
        
        # # Store the summary and generate a unique ID for tracking
        # unique_id = uuid.uuid4()
        # #Complaint.objects.create(customer=customer, summary=complaint_summary, unique_id=unique_id)

        # # Display the unique ID to the customer
        # print(f"Complaint successfully logged. Your unique ID is: {unique_id}")
