# chatbot_app/management/commands/chatbot_interaction.py
import argparse
import uuid
from django.core.management.base import BaseCommand
#from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


from chatbot_app.models import Customer, ChatMessage, Complaint
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Interact with customers using a chatbot'

    def handle(self, *args, **options):

        while True:
            # Get customer information
            name = input("Enter customer name: ")
            phone_number = input("Enter phone number: ")
            email = input("Enter email address: ")
            address = input("Enter customer address: ")

            # Create a customer instance
            customer = Customer(name=name, phone_number=phone_number, email=email, address=address)

            try:
                # Trigger model validation
                customer.full_clean()
                break  # Break the loop if validation succeeds
            except ValidationError as e:
                print(f"Validation error: {e}")
                print("Please re-enter the information.")

        # Save the instance to the database
        customer.save()

        # Initialize the T5 transformer
        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")


        #create the interactive chat
        conversation = ""
        while True:
            user_input=input("You: ")
            if user_input.lower() == 'exit':
               break
            # Formulate the prompt with the summarization instruction
            prompt = f"Answer the following question:\n{user_input}"
            inputs = tokenizer(prompt, return_tensors="pt")
            outputs = model.generate(**inputs,max_length=500)
            chatbot_response=tokenizer.batch_decode(outputs, skip_special_tokens=True)
            print(f"Chatbot: {chatbot_response}")

            conversation += f"User: {user_input}\n"
            conversation += f"chatbot: {chatbot_response}\n"


        # Log the chat message
        chat_message=ChatMessage.objects.create(customer=customer, message=conversation)
        chat_message.save()

        inputs = tokenizer("Summarize: "+conversation, return_tensors="pt")
        outputs = model.generate(**inputs,max_length=500)
        complaint_summary=tokenizer.batch_decode(outputs, skip_special_tokens=True)
        print(f"summary: {complaint_summary}")
        # Store the summary and generate a unique ID for tracking
        unique_id = uuid.uuid4()
        complaint=Complaint.objects.create(customer=customer, summary=complaint_summary, unique_id=unique_id)

        # Display the unique ID to the customer
        print(f"Complaint successfully logged. Your unique ID is: {unique_id}")
        complaint.save()



