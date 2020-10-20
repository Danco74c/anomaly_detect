from elasticsearch import Elasticsearch
import configparser
import time
import requests
import json


def queryElastic(ip,port):
    print("Connecting to ElasticSearch to query event count. IP: " + ip + " PORT: " + port)
    es = Elasticsearch([ip], port=port)
    query = {
        "query" : {
            "range" : {
                "@timestamp" : {
                    "gte" : "now-20s"
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


config = configparser.ConfigParser()
config.readfp(open(r'config'))




starttime = time.time()
print("Entering polling loop")

elasticIp = config.get('Elastic', 'ip')
elasticPort = config.get('Elastic', 'port')

modelServiceIp = config.get('Model Service', 'ip')
modelServicePort = config.get('Model Service', 'port')

while True:
    currentEventCount = -1
    try:

        currentEventCount = queryElastic(elasticIp,elasticPort)
        print(currentEventCount)
    except Exception as e:
        print(e)
        print("failed to query event count from ElasticSearch")

    if (currentEventCount != -1):
        try:    
            output = analyze(modelServiceIp,modelServicePort,currentEventCount)
            print(output)
        except Exception as e:
            print(e)
            print("Failed to retrieve data from to the model service")
    
    print("tick")
    time.sleep(5 - ((time.time() - starttime) % 5))
    






