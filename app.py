from elasticsearch import Elasticsearch
import configparser
import time
import datetime
import requests
import json
import csv
import os
import logging
import boto3
from botocore.exceptions import ClientError

#xxx


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
    )
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def queryElastic(ip,port):
    print("Connecting to ElasticSearch to query event count. IP: " + ip + " PORT: " + port)
    es = Elasticsearch([ip], port=port)
    query = {
        "query" : {
            "range" : {
                "@timestamp" : {
                    "gte" : "now-30s"
                    }
                }
            }
    }

    res = es.count(index="syslog-received-on-tcp", body=query)
    return res['count']

def analyze(ip,port,eventCount):
    url = "http://" + str(ip) + ":" + str(port) + "/report"
    print("Connecting to Model Service to get analasis. URL: " + url + " EVENTS: " + str(eventCount))
    myobj = {"eventCount": eventCount}
    print(myobj)
    headers = {'content-type': 'application/json'}
    req = requests.post(url, json = myobj, headers = headers)
    return json.loads(req.text)




starttime = time.time()
print("Entering polling loop")


print(os.environ.get('MODEL_SERVICE_IP'))

while True:

    fileName = str(datetime.datetime.now().timestamp()) + '.csv'
    print(fileName)
    csvFile = open(fileName,"w+",newline='')
    writer = csv.writer(csvFile, delimiter=',')

    recordCount = 0

    while recordCount < int(os.environ.get('RECORDS_PER_FILE')):
        currentEventCount = -1
        try:

            currentEventCount = queryElastic((os.environ.get("ELASTIC_IP")),os.environ.get("ELASTIC_PORT"))
            writer.writerow([datetime.datetime.now().timestamp(),currentEventCount])
            recordCount += 1
            
        except Exception as e:
            print(e)
            print("failed to query event count from ElasticSearch")

        if (currentEventCount != -1):
            try:    
                output = analyze(os.environ.get("MODEL_SERVICE_IP"),os.environ.get("MODEL_SERVICE_PORT"),currentEventCount)
                print(output)
            except Exception as e:
                print(e)
                print("Failed to retrieve data from to the model service")
        
        print("tick")
        time.sleep(int(os.environ.get('TIME_INTERVAL')) - ((time.time() - starttime) % int(os.environ.get('TIME_INTERVAL'))))
        csvFile.flush()
    
    csvFile.close()
    upload_file(fileName,"danco-anomaly-detection",'event-count/{}'.format(fileName))



    






