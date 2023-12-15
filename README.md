# Customer Chatbot CLI Application

Welcome to the Customer Chatbot CLI Application! This application incorporates a chatbot to interact with customers, collect their information, and log chat messages. The chatbot is powered by the T5 transformer, and customer data is stored in a MySQL database.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Database Schema](#database-schema)
4. [Instructions for Running the CLI Application](#instructions-for-running-the-cli-application)


## 1. Overview

This CLI application provides a simple and efficient way to interact with customers using a chatbot. It covers customer information collection, chat logging, complaint summary generation, and unique ID assignment for tracking.

## 2. Architecture

### Components:

- **CLI Application:**
  - A command-line interface for interacting with the chatbot.
  
- **Chatbot Integration:**
  - Utilizes the T5 transformer for natural language interactions.

- **Customer Information Collection:**
  - Collects customer details such as name, phone number, email, and address.

- **Chat Logging:**
  - Logs all chat messages in the MySQL database.

- **Complaint Summary Generation:**
  - Generates a summary of the customer's problem using the T5 model.

- **Unique ID Generation:**
  - Assigns a unique ID for tracking each complaint.

## 3. Database Schema

### Tables:

- **Customer:**
  - Fields: `id`, `name`, `phone_number`, `email`, `address`

- **ChatMessage:**
  - Fields: `id`, `customer`, `message`

- **Complaint:**
  - Fields: `id`, `customer`, `summary`, `unique_id`

### Relationships:

- `ChatMessage.customer` is a foreign key referencing `Customer.id`.
- `Complaint.customer` is a foreign key referencing `Customer.id`.

### Data Validation:

- Phone numbers and email addresses are validated for correct formats.

## 4. Instructions for Running the CLI Application

### Dependencies:

- Django
- Transformers library


