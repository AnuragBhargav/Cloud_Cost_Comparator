from flask import Flask, render_template, request

from src.app.database.instances import aws, gcp


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

    cloud_regions = {
        "GCP": {
            "US Central": ["us", "us", "us-central1"],
            "US East": ["us-east", "us-east1", "us-east4"],
            "US West": ["us-west", "us-west1", "us-west2", "us-west3", "us-west4"],
        },
        "AWS": {
            "US Central": ["US Central"],
            "US East": ["US East", "US East (Ohio)", "US East (Northern Virginia)", "GovCloud (US-East)"],
            "US West": ["US West", "US West (Oregon)", "US West (Northern California)", "GovCloud (US-West)"],
        },
        "AZURE": {}
    }

    aws_region = cloud_regions["AWS"][instance_details["region"]][0]
    gcp_region = cloud_regions["GCP"][instance_details["region"]][0]

    aws_instances_details = aws.get_instance_details(instance_details, aws_region)
    gcp_instances_details = gcp.get_instance_details(instance_details, gcp_region)

    # print(aws_instances_details)
    # print(gcp_instances_details)

    html_data[0]["price"] = float(instance_details["no-of-instances"]) * float(instance_details["avg-days-per-week"]) * (float(instance_details["avg-hours-per-day"]) * float(gcp_instances_details[-1]))
    html_data[1]["price"] = float(instance_details["no-of-instances"]) * float(instance_details["avg-days-per-week"]) * (float(instance_details["avg-hours-per-day"]) * float(aws_instances_details[-1]))

    html_data[0]["details"] = {
        "machine_type": gcp_instances_details[1],
        "memory": gcp_instances_details[4],
        "vcpus": gcp_instances_details[3],
        "region": gcp_instances_details[2]
    }

    html_data[1]["details"] = {
        "memory": aws_instances_details[2],
        "vcpus": aws_instances_details[3],
        "machine_type": aws_instances_details[4],
        "region": aws_instances_details[5]
    }

    return render_template("instance-calculator.html", html_data=html_data)


if __name__ == "__main__":
    app.run("localhost", port=9191, debug=True)
