import os

#ELASTIC PARAMS
ELASTIC_IP = os.environ.get("ELASTIC_IP")
ELASTIC_PORT = os.environ.get("ELASTIC_PORT")
ELASTIC_USER = os.environ.get("ELASTIC_USER")
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")

#MODEL PARAMS
MODEL_SERVICE_IP = os.environ.get("MODEL_SERVICE_IP")
MODEL_SERVICE_PORT = os.environ.get("MODEL_SERVICE_PORT")

#VROPS PARAMS
VROPS_IP = os.environ.get("VROPS_IP")
VROPS_PORT = os.environ.get("VROPS_PORT")
VROPS_OBJID = os.environ.get("VROPS_OBJID")
VROPS_USER = os.environ.get("VROPS_USER")
VROPS_PASSWORD = os.environ.get("VROPS_PASSWORD")

#ANALYZE
TIME_INTERVAL = int(os.environ.get("TIME_INTERVAL"))
RECORDS_PER_FILE = int(os.environ.get('RECORDS_PER_FILE'))

#AWS
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')