import pandas as pd
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

def handle_email(parameter):
    global email1
    email1 = parameter['email']

    csv_file_path = "return.csv"

    # Create a DataFrame with sample data (if the file doesn't exist yet)
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['order_id', 'reason', 'condition', 'replace/refund', 'email'])

    # Example data to insert
    new_row_data = {"order_id": order_id1, "reason": reason1, "condition": cond1, "replace/refund": replacerefund1,
                    "email": email1}

    # Append the new row to the DataFrame
    df = df.append(new_row_data, ignore_index=True)

    # Write the DataFrame back to the CSV file
    df.to_csv(csv_file_path, index=False, mode='w' if 'order_id' not in df.columns else 'a',
              header=not ('order_id' in df.columns and len(df) > 0))


