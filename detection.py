from elasticsearch import Elasticsearch
from helper import query_elastic,send_event_metrics,analyze
import time
import datetime
import params



def start_detection(hosts,writer,time_interval,records):

    print("Entering polling loop")
    starttime = time.time()
    record_count = 0

    while record_count < int(records):   

        try:
            elastic_results = query_elastic(params.ELASTIC_IP,params.ELASTIC_PORT,hosts,user=params.ELASTIC_USER,password=params.ELASTIC_PASSWORD)
            print(elastic_results)
            writer.writerow(elastic_results)
            record_count += 1
            
        except Exception as e:
            print(e)
            print("failed to query event count from ElasticSearch")

        try:    
            analysis = analyze(params.MODEL_SERVICE_IP,params.MODEL_SERVICE_PORT,elastic_results) 
            print(analysis)      
        except Exception as e:
            print(e)
            print("Failed to retrieve data from to the model service")

        #send_event_metrics(params.VROPS_IP,params.VROPS_PORT,analysis,int(time.time()*1000),params.VROPS_USER,params.VROPS_PASSWORD)
        time.sleep(time_interval - ((time.time() - starttime) % time_interval))
