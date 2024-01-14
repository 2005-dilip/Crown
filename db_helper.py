import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(user='root', password='root', host='localhost', port='3306', database='pandeyji_eatery')


def get_order_status(order_id):
    cursor = connection.cursor()

    # Define the SQL query to retrieve the status for a given order_id
    query = "SELECT status FROM order_tracking WHERE order_id = %s"

    # Execute the query with the provided order_id
    cursor.execute(query, (order_id,))

    # Fetch the result
    result = cursor.fetchone()
    if result:
        # Extract the status from the result
        status = result[0]
        return status
    else:
        return None  # Order ID not found