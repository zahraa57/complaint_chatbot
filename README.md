# Customer Chatbot CLI Application

Welcome to the Customer Chatbot CLI Application! This application incorporates a chatbot to interact with customers, collect their information, and log chat messages. The chatbot is powered by the T5 transformer, and customer data is stored in a MySQL database.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Database Schema](#database-schema)
4. [Instructions for Running the CLI Application](#instructions-for-running-the-cli-application)
5. [Usage Examples](#usage-examples)


## 1. Overview

This CLI application provides a simple and efficient way to interact with customers using a chatbot. It covers customer information collection, chat logging, complaint summary generation, and unique ID assignment for tracking.

## 2. Architecture

### Components:

- **CLI Application:**
  - A command-line interface for interacting with the chatbot.
  
- **Chatbot Integration:**
  - Utilizes the `google/flan-t5-small` transformer for natural language interactions.

- **Customer Information Collection:**
  - Collects customer details such as name, phone number, email, and address.

- **Chat Logging:**
  - Logs all chat messages in the MySQL database.

- **Complaint Summary Generation:**
  - Generates a summary of the customer's problem using the `Tgoogle/flan-t5-small` model.

- **Unique ID Generation:**
  - Assigns a unique ID for tracking each complaint.

## 3. Database Schema

### Tables:

- **Customer:**
  - Fields: `id`, `name`, `phone_number`, `email`, `address`

- **ChatMessage:**
  - Fields: `id`, `customer`, `message`, `timestamp`

- **Complaint:**
  - Fields: `id`, `customer`, `summary`, `unique_id`

### Relationships:

- `ChatMessage.customer` is a foreign key referencing `Customer.id`.
- `Complaint.customer` is a foreign key referencing `Customer.id`.

### Data Validation:

- Phone numbers and email addresses are validated for correct formats.
- for email address used `EmailValidator` from `django.core.validators` 
- for phone validation  created simple function `validate_phone_number` 

## 4. Instructions for Running the CLI Application

### Dependencies:

- Django
- Transformers library
- to run the CLI run this command: `python manage.py chatbot_interaction`

## 5. Usage Examples

- Input customer information when prompted.
- Engage in a chat with the chatbot.
- create complaint summaries with a unique ID provided.

You: Could I make a complaint as The connection is poor and what shoul I do?
Chatbot: I don't understand what it means
You: The internet is bad what should I do?
Chatbot: Use a mobile phone
You: The signal is not good
Chatbot: Seja
You: can you help me?
Chatbot: Yes
You: How to make tea?
Chatbot: Pour boiling water and ice cubes into a tea glasses. Pour as much water as you want, and let steep for 3 minutes.
You: exit
summary: Chatbot: You can use a mobile phone to make tea.

- it may be fine tuned with customer real complaints and answers for better behaviour.

