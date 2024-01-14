import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
order_id1=0
reason1=''
cond1=''
replacerefund1=''
email1=''
def handle_orderid(parameter):
    global order_id1
    order_id1 = int(parameter['number'])

def handle_reason(parameter):
    global reason1
    reason1 = parameter['reason']

def handle_condition(parameter):
    global cond1
    cond1 = parameter["condition"][0]

def handle_replacerefund(parameter):
    global replacerefund1
    replacerefund1 = parameter["refundreplace"][0]

def handle_email1(parameter):
    global email1
    email1 = parameter['email']

    csv_file_path = "return.csv"
    new_row_data = {"order_id": order_id1, "reason": reason1, "condition": cond1, "replace/refund": replacerefund1,
                    "email": email1}
    order_id =order_id1
    reason=reason1
    con=cond1
    replacerefund=replacerefund1
    email = email1
    sender_email = "crownweb37@gmail.com"
    sender_password = "jcoo xafd uqdu pvzl"  # Generate an App Password for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    if replacerefund=='Replace':
        subject = f"Update on Replace Request - Order {order_id}"
        body = f"Dear Customer,\n\nYour Replace request for Order ID {order_id} is currently under review.\n\nDetails:\nReason: {reason}\nCondition: {con}\nReplace/Refund: {replacerefund}\n\nThank you for choosing our service!\n\nBest regards,\nCustomer Support Team"
    elif replacerefund=='Refund':
        subject = f"Update on Refund Request - Order {order_id}"
        body = f"Dear Customer,\n\nYour Refund request for Order ID {order_id} is currently under review.\n\nDetails:\nReason: {reason}\nCondition: {con}\nReplace/Refund: {replacerefund}\n\nThank you for choosing our service!\n\nBest regards,\nCustomer Support Team"

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

        pass
    except Exception as e:
        pass

    pass
    return insert_row(csv_file_path,new_row_data)

def insert_row(csv_file_path, row_data):
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['order_id', 'reason', 'condition', 'replace/refund', 'email']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write data row
        writer.writerow(row_data)

