
from datetime import datetime
import requests
import re
import mysql.connector

now = datetime.now()

dt_tym = now.strftime("%Y-%m-%d %H:%M:%S")

print(dt_tym)

ru = requests.get("https://cloudpricingcalculator.appspot.com/static/data/pricelist.json")

ruc = ru.json()

# print(ruc)
k = ruc['gcp_price_list'].keys()

machine_types = []

for i in k:
    # print(i)
    if (re.search('^CP-COMPUTEENGINE-VMIMAGE',i)):
        # print(i)
        machine_types.append(i)

print(machine_types)

region=['us', 'us-central1', 'us-east1', 'us-east4', 'us-west4', 'us-west1', 'us-west2', 'us-west3', 'europe', 'europe-west1', 'europe-west2', 'europe-west3', 'europe-west4', 'europe-west6', 'europe-north1', 'northamerica-northeast1', 'asia', 'asia-east', 'asia-east1', 'asia-east2', 'asia-northeast', 'asia-northeast1', 'asia-northeast2', 'asia-northeast3', 'asia-southeast', 'asia-southeast1', 'australia-southeast1', 'australia', 'southamerica-east1', 'asia-south1', 'asia-southeast2']
# print(ruc['gcp_price_list'])

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",                  # Change this password
        database="GCP"
    )
mycursor = mydb.cursor()

for i in machine_types:
    for j in region:
        print(i)
        print(j)
        print(ruc['gcp_price_list']['{}'.format(i)]["{}".format(j)])
        sql = "INSERT into instances (date,machine_type,region,cost_per_hr) VALUES (%s,%s,%s,%s)"
        val = (dt_tym,i,j,ruc['gcp_price_list']['{}'.format(i)]["{}".format(j)])
        mycursor.execute(sql, val)
        mydb.commit()

