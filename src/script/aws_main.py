import boto3
import json
import pprint
import mysql.connector
from datetime import datetime

session = boto3.Session(
    aws_access_key_id="AKIA4TFPTNUIO7B3A3YM",
    aws_secret_access_key="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",
    region_name="us-east-1"
)

client = session.client("pricing")

response = client.get_products(
    ServiceCode="AmazonEC2",
)

now = datetime.now()

dt_tym = now.strftime("%Y-%m-%d %H:%M:%S")


# print(response)
#
# print(response["PriceList"])
#
# print(response["PriceList"][0])

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Anurag@123",
        database="AWS"
    )
mycursor = mydb.cursor()


for r in range(500):

    try:
        lo = json.loads(response["PriceList"][r])
        # print(type(lo))

        memory_c = lo["product"]["attributes"]["memory"]
        v_cpu = lo["product"]["attributes"]["vcpu"]
        instance_type = lo["product"]["attributes"]["instanceType"]
        location = lo["product"]["attributes"]["location"]

        term_keys = lo["terms"].keys()
        # print(term_keys)

        terms_list = []

        for i in term_keys:
            terms_list.append(i)
        # print(terms_list)


        for t in terms_list:

            # print(lo["terms"]["OnDemand"])
            key_c = lo["terms"][t].keys()

            keys_list_c = []

            for i in key_c:
                keys_list_c.append(i)
            # print(keys_list_c)

            keys_list_index_c = keys_list_c[0]


            key_d = lo["terms"][t][keys_list_index_c]["priceDimensions"].keys()

            keys_list_d = []

            for j in key_d:
                keys_list_d.append(j)
            # print(keys_list_d)

            keys_list_index_d = keys_list_d[0]



            price_usd = lo["terms"][t][keys_list_index_c]["priceDimensions"][keys_list_index_d]["pricePerUnit"]["USD"]

            print(t,memory_c,v_cpu,instance_type,location,price_usd)


            sql = "INSERT into instances (date,type_m,memory_in,vcpu,machine_type,region,cost_per_hr) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (dt_tym, t, memory_c, v_cpu,instance_type,location,price_usd)
            mycursor.execute(sql, val)
            mydb.commit()
            print(r)

    except:
        pass