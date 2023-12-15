# chatbot_app/management/commands/chatbot_interaction.py
import argparse
import uuid
from django.core.management.base import BaseCommand
from transformers import T5ForConditionalGeneration, T5Tokenizer
#from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from chatbot_app.models import Customer, ChatMessage, Complaint
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Interact with customers using a chatbot'

    def handle(self, *args, **options):
        # Get customer information
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
        model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
        tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small",legacy=True)


        #create the interactive chat
        conversation = ""
        while True:

            user_input=input("You: ")

            if user_input.lower() == 'exit':
               break
               

            # Formulate the prompt with the summarization instruction
            # Customize prompt based on user input
            if "help" in user_input.lower():
                prompt = f"You are the customer support assistant.\n{user_input}"
            else:
                prompt = f"Reasonaly answer the following question:\n{user_input}"

            inputs = tokenizer(prompt, return_tensors="pt")

            outputs = model.generate(**inputs,
                                     max_length=500,
                                     temperature=0.7,
                                     num_beams=1,
                                     do_sample=True)
            
            chatbot_response=tokenizer.batch_decode(outputs, skip_special_tokens=True)
            print(f"Chatbot: {chatbot_response[0]}")

            conversation += f"User: {user_input}\n"
            conversation += f"chatbot: {chatbot_response[0]}\n"


        # Log the chat message
        chat_message=ChatMessage.objects.create(customer=customer, message=conversation)
        chat_message.save()
        
        #Create the chat summary
        inputs = tokenizer("Summarize: "+conversation, return_tensors="pt")
        outputs = model.generate(**inputs,max_length=500)
        complaint_summary=tokenizer.batch_decode(outputs, skip_special_tokens=True)
        print(f"summary: {complaint_summary[0]}")
        # Store the summary and generate a unique ID for tracking
        unique_id = uuid.uuid4()
        complaint=Complaint.objects.create(customer=customer, summary=complaint_summary, unique_id=unique_id)

        # Display the unique ID to the customer
        print(f"Complaint successfully logged. Your unique ID is: {unique_id}")
        complaint.save()



