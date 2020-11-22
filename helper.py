from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth
import time
import datetime
import requests
import json
import logging

#aws packages
import boto3
from botocore.exceptions import ClientError
#params
import params


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client(
    's3',
    aws_access_key_id=params.AWS_ACCESS_KEY,
    aws_secret_access_key=params.AWS_SECRET_KEY
    )
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return response

def send_event_metrics(ip,port,hosts_data,timestamp,user,password):

    results = []
    for host in hosts_data:
        url = "https://" + str(ip) + ":" + str(port) + "/suite-api/api/resources/" + host["id"] + "/stats"
        body = '''{
        "stat-content" : [ {
            "statKey" : "CustomMetrics|MLEvents|Anomaly",
            "timestamps" : [],
            "data" : [],
            "others" : [],
            "otherAttributes" : { }
        }]
        }'''
        body_obj = json.loads(body)
        body_obj["stat-content"][0]["timestamps"].append(timestamp)
        body_obj["stat-content"][0]["data"].append(host["anomaly_prct"])
        headers = {'content-type': 'application/json'}
        req = requests.post(url, json = body_obj, headers = headers, verify=False, auth=(params.VROPS_USER,params.VROPS_PASSWORD))
        results.append(req)
    return results

def get_hosts(ip,port,user,password):
        url = "https://" + str(ip) + ":" + str(port) + "/suite-api/api/resources?resourceKind=hostsystem"
        headers = {'content-type': 'application/json','accept': 'application/json'}
        req = requests.get(url, headers = headers, verify=False, auth=(params.VROPS_USER,params.VROPS_PASSWORD))
        obj = json.loads(req.content)
        host_objs = (obj["resourceList"])
        hosts = []
        for obj in host_objs:
            host = {}
            host["name"] = obj["resourceKey"]["name"]  
            host["id"] = obj["identifier"]
            hosts.append(host)
        return hosts


def query_elastic(ip,port,hosts,user,password):
    print("Connecting to ElasticSearch to query event count. IP: " + ip + " PORT: " + port)
    es = Elasticsearch([ip], port=port)
    results = []
    for host in hosts:
        req_body = {"query": {"bool": {"must": [{"match_phrase": {"syslog_hostname": host["name"]}},{"range" : {"@timestamp" : {"gte" : "now-30s"}}}]} }}
        response = es.count(index='syslog-received-on-tcp',body=req_body)
        results.extend([{"name": host["name"], "id": host["id"], "count": response['count']}])

    return results

def analyze(ip,port,data):
    url = "http://" + str(ip) + ":" + str(port) + "/report"
    print("Connecting to Model Service to get analasis")
    headers = {'content-type': 'application/json'}
    req = requests.post(url, json = data, headers = headers)
    return json.loads(req.text)