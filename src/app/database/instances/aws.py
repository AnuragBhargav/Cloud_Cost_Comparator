import os
import mysql.connector
from mysql.connector import Error


def get_instance_details(instance_details, region):
    mydb = None
    row = None

    #
    # Connect to DB
    #
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=os.environ.get("DB_USERNAME"),
            passwd=os.environ.get("DB_PASSWORD"),
            database="AWS"
        )
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM instances WHERE memory_in>={0} && vcpu >= {1} && region REGEXP '^{2}' && cost_per_hr!=0 ORDER BY memory_in ASC LIMIT 1".format(instance_details["memory"], instance_details["vcpus"], region))

        row = mycursor.fetchone()

    except Error as e:
        print(e)

    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

    if row is None:
        return ["None", "None", "None", "None", "None", "None", 0]
    else:
        return row
