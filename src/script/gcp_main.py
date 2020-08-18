import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv
from datetime import datetime
import requests
import re
import mysql.connector
from mysql.connector import Error

#
# dot env configuration
#
dotenv_path = abspath(join(dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)


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
        user=os.environ.get("DB_USERNAME"),
        passwd=os.environ.get("DB_PASSWORD"),
        database="GCP"
    )
mycursor = mydb.cursor()

for i in machine_types:
    for j in region:
        try:
            print(i)
            print(j)
            cost_p = ruc['gcp_price_list']['{}'.format(i)]["{}".format(j)]
            cores_p = ruc['gcp_price_list']['{}'.format(i)]["cores"]
            memory_p = ruc['gcp_price_list']['{}'.format(i)]["memory"]
            print(ruc['gcp_price_list']['{}'.format(i)]["{}".format(j)])
            print(ruc['gcp_price_list']['{}'.format(i)]["cores"])
            print(ruc['gcp_price_list']['{}'.format(i)]["memory"])


            sql = "INSERT into instances (date,machine_type,region,vcpu,memory_in,cost_per_hr) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (dt_tym,i,j,cores_p,memory_p,cost_p)
            mycursor.execute(sql, val)
            mydb.commit()
        except:
            # print(e)
            pass

