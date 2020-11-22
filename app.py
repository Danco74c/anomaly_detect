from helper import get_hosts,upload_file
from detection import start_detection
import csv
import datetime
import time
import params
import json

while True:

    file_name = str(datetime.datetime.now().timestamp()) + '.csv'

    #open csv file for writing
    csv_file = open(file_name,"w+",newline='')
    csv_writer = csv.writer(csv_file, delimiter=',')

    #get hosts
    hosts = get_hosts(params.VROPS_IP,params.VROPS_PORT,user=params.VROPS_USER,password=params.VROPS_PASSWORD)

    #start analysis loop
    start_detection(hosts,csv_writer,params.TIME_INTERVAL,params.RECORDS_PER_FILE)

    #close file
    csv_file.flush()
    csv_file.close()
    upload_file(file_name,"danco-anomaly-detection",'event-count/{}'.format(file_name))
