import smtplib
import random
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from watch_list import watch_brands
import pandas as pd
from return_watches import *
app = FastAPI()
items = []
order_id1=[]
@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    # Route the call to the appropriate intent handler function
    if intent == "track-order-ongoing-tracking":
        return handle_track_order(parameters)
    elif intent == "order.add-ongoing-order":
        return handle_add_ongoing_order(parameters)
    elif intent == "more_options":
        return handle_more_options(parameters)
    elif intent=='email':
        return handle_email(parameters)
    elif intent=='customer_support':
        return handle_customer_support()
    elif intent=='p_return - Order ID':
        return handle_orderid(parameters)
    elif intent=='p_return - Reason for Return':
        return handle_reason(parameters)
    elif intent=='p_return - Reason for Return - condition1':
        return handle_condition(parameters)
    elif intent=='p_return - Reason for Return - condition1 - replacerefund':
        return handle_replacerefund(parameters)
    elif intent=='p_return - Reason for Return - condition1 - replacerefund - email':
        return handle_email1(parameters)
def handle_customer_support():
    fulfillment_response = {
        "fulfillmentMessages": [
            {
                "quickReplies": {
                    "title": "Please select an option:",
                    "quickReplies": [
                        "Return Information",
                        "Exchange Information",
                        "Warranty Inquiry"
                    ]
                }
            }
        ]
    }

    return JSONResponse(content=fulfillment_response)
def generate_random_timestamp():
    # Generate a random timestamp within the past week
    current_time = datetime.datetime.now()
    random_days = random.randint(1, 7)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)

    random_timestamp = current_time - datetime.timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
    return random_timestamp.strftime("%Y-%m-%d %H:%M:%S")
def handle_email(parameters):
    df = pd.read_csv("orders.csv", index_col='order_id')
    order_id=order_id1[-1]
    email = parameters["email"]
    order_status = df['status'][order_id]
    sender_email = "crownweb37@gmail.com"
    sender_password = "jcoo xafd uqdu pvzl"  # Generate an App Password for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    random_timestamp = generate_random_timestamp()
    # Create a message
    if order_status.lower() == "delivered":
        subject = f"Order {order_id} Status: {order_status}"
        body = f"Order ID {order_id} is {order_status} on {random_timestamp}."

    elif order_status.lower() == "in transit":
        subject = f"Order {order_id} Status: {order_status}"
        body = f"Order ID {order_id} is {order_status} it will be delivered on {random_timestamp}."
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Log in to your email account
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, email, message.as_string())

        response = {"fulfillmentText": f"Email sent to {email} successfully."}
    except Exception as e:
        response = {"fulfillmentText": f"Error sending email: {str(e)}"}

    return JSONResponse(content=response)

def handle_track_order(parameters):
    df = pd.read_csv("orders.csv",index_col='order_id')
    order_id = int(parameters['number'])
    order_id1.append(order_id)
    order_status = df['status'][order_id]
    if order_status:
        response = {"fulfillmentText": f"The Order Status for Order ID: {order_id} is {order_status}\nWould you like to track your orders with notifications?\nIf yes, please provide your email address."}
    else:
        response = {"fulfillmentText": f"No order found with order id: {order_id}"}
    return JSONResponse(content=response)

def handle_add_ongoing_order(parameters):
    order_item = parameters["watch-item"]
    items.append(order_item)
    description = watch_brands[order_item]["description"]
    mod = watch_brands[order_item]['models']
    mat = watch_brands[order_item]['materials']
    price = watch_brands[order_item]["starting_price"]

    response = {
        "fulfillmentText": f"{description}\n[You can say more as an input to get more info!]",
        "messages": [
            {
                "card": {
                    "title": "Watch Details",
                    "subtitle": description,
                    "buttons": [
                        {
                            "text": "More",
                            "postback": "More options"
                        }
                    ]
                }
            }
        ]
    }

    return JSONResponse(content=response)

def handle_more_options(parameters):
    watch_item = items[-1]

    if watch_item in watch_brands:
        models_value = watch_brands[watch_item]['models']
        materials_value = watch_brands[watch_item]['materials']
        price_value = watch_brands[watch_item]["starting_price"]
        features_dict = watch_brands[watch_item]['features']
        if isinstance(models_value, dict):
            models_value=list(models_value.keys())
        l = list(watch_brands[watch_item]['features'].keys())
        # Build concise features list with key points
        watch_features_string = l

        # Materials Section
        materials_section = {
            "type": "accordion",
            "title": "Materials",
            "subtitle": "Click the Options for more info.",
            "text": [f"{material}\n" for material in materials_value]
        }

        # Models Section
        models_section = {
            "type": "accordion",
            "title": "Models",
            "subtitle": "Click the Options for more info.",
            "text": [f"{model}\n" for model in models_value]
        }

        # Price Section
        price_section = {
            "type": "accordion",
            "title": "Price",
            "subtitle": "Click the Options for more info.",
            "text": [f"Starting Price is from {price_value}\n"]
        }

        # Watch Features Section
        watch_features_section = {
            "type": "accordion",
            "title": "Watch Features",
            "subtitle": "Click the Options for more info.",
            "text": [f"{feature}\n" for feature in watch_features_string]
        }

        response = {
            "fulfillmentMessages": [
                {
                    "payload": {
                        "richContent": [
                            [materials_section],
                            [models_section],
                            [price_section],
                            [watch_features_section]
                        ]
                    }
                }
            ]
        }

        return response
    else:
        return {"fulfillmentText": f"No information found for watch item: {watch_item}"}
