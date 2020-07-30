from flask import Flask, render_template, request
import os

import mysql.connector
from mysql.connector import Error


app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("instances.html")


@app.route("/instanceCalculator", methods=["POST"])
def instance_calculator():
    instance_details = request.form
    html_data = [
        {
            "cloudName": "GCP",
            "price": "",
            "details": {}
        },
        {
            "cloudName": "AWS",
            "price": "",
            "details": {}
        }
    ]

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

        mycursor.execute("SELECT * FROM instances WHERE memory_in>={0} && vcpu >= {1} && cost_per_hr!=0 ORDER BY memory_in ASC LIMIT 1".format(instance_details["memory"], instance_details["vcpus"]))
        row = mycursor.fetchone()
        print(row)

        html_data[1]["price"] = float(instance_details["no-of-instances"]) * float(instance_details["avg-days-per-week"]) * (float(instance_details["avg-hours-per-day"]) * float(row[-1]))

        html_data[1]["details"] = {
            "type_m": row[1],
            "memory": row[2],
            "vcpus": row[3],
            "machine_type": row[4],
            "region": row[5]
        }

    except Error as e:
        print(e)

    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

    return render_template("instance-calculator.html", html_data=html_data)


if __name__ == "__main__":
    app.run("localhost", port=9191, debug=True)
