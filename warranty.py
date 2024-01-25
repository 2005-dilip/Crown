import smtplib
import random
from email.mime.text import MIMEText
from fastapi.responses import JSONResponse
from email.mime.multipart import MIMEMultipart
import datetime
message=["'Thank you for the details. We'll review the information. Is there anything else you'd like to ask?'","We appreciate your input. We'll assess the information you provided. Is there anything additional you want to mention?","Your details have been received. We'll now proceed with the assessment. Do you have any other questions ?","Thanks for providing the information. We'll review it shortly. Is there anything else you'd like to include or inquire about?","Your input is noted. We'll be reviewing the details. Is there any additional information you think would be like to ask ?"]
orderid=[]
date=[]
def warranty_orderid(parameters):
    order_id1 = int(parameters['number'])
    orderid.append(order_id1)
def warranty_date(parameters):
    date_time_str = parameters["date-time"]
    date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S%z")
    date_only = date_time_obj.date()
    date.append(date_only)
def warranty_email(parameters):
    email = parameters['email']
    sender_email = "crownweb37@gmail.com"  # Replace with your email
    receiver_email = email
    password = "jcoo xafd uqdu pvzl"  # Replace with your email password
    body = (
        f"Thank you for reaching out. We have received your warranty claim.\n\n"
        f"Order ID: {orderid[-1]}\nPurchase Date: {date[-1]}\n\n"
        "We appreciate your cooperation. "
        "Rest assured, our team is reviewing the information you provided, including the proof video of your product's issue. "
        "If you have any further questions or concerns, feel free to reach out.\n\n"
        "Best regards,\nTeam Crown"
    )

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Warranty Claim Information'
    msg.attach(MIMEText(body, 'plain'))



    # Establish connection with the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

    # Return JSON response with a random message
    return JSONResponse(content={"fulfillmentText": f"{random.choice(message)}"})
