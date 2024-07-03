#Importing YAML module to handle yaml config files
import yaml 
#Importing JSON module to handle jsons
import json  
#Importing OS module to interact with OS
import os
#Importing glob module to find all yaml files in the cureent working directory
import glob 
#Importing Flask module and jsonify to handle json response
from flask import Flask,jsonify  
# Importing MongoClient for the interaction with MongoDB
from pymongo import MongoClient  
from bson import json_util

#Initializing the Flask application
app = Flask(__name__)

#Connecting to MongoDB using connection string 
client = MongoClient('mongodb://localhost:27017/')

#Name of the data base "myconfigdata"
db = client['myconfigdata']

#Name of the collection inside the Databse "myconfigdata"
collection = db['configs']

#MongoDb connection successfull or not
@app.route('/')
def index():
        client.server_info()  
        return "Welcome to Flask App...Connection successfull with MongoDB...!"
        
#API to fetch pushed yaml config into your browser
@app.route('/configs', methods=['GET'])
def configs_yaml():
        #taking data from the collection inside the DB
        sensitive_json = collection.find({})
        configuartions = list(sensitive_json)
        
        #getting the response back from mongoDB and handelling the incoming json response:)
        get_request = json_util.dumps(configuartions)
        return jsonify(get_request)

#Function to insert the spcific sensitive data to mongoDB
def insert():
     
    try:


        #loading the current working directory
        current_directory = os.getcwd()  
        #Searching for all yaml files in the current working directory
        yaml_files = glob.glob(os.path.join(current_directory, "*.yaml"))
        if yaml_files:
            print("Configuation(yaml files) files found.")
            #Processing each yaml file to extract the sensitive info
            for file in yaml_files:
                try:
                    with open(file, 'r') as config:
                        #Converting yaml to dataset dict
                        yaml_dict = yaml.safe_load(config)
                        #fetching only the basename of the yaml file
                        basename,extension = os.path.splitext(file)
                        #Initializing an empty dict. with the same name as the filename
                        basename = {}
                        #Fetching few sensitive info and pushig it to dataset dict
                        basename["username"] = yaml_dict["Database"]["username"]
                        basename["password"] = yaml_dict["Database"]["password"]
                        basename["server_address"] = yaml_dict["Server"]["address"]
                        yaml_to_json = json.dumps(basename, indent=1)
                        print(yaml_to_json)
                        #creating json and writing to it.
                        json_file = open(f"{os.path.basename(file)}.json", "w")  
                        
                        json_file.write(yaml_to_json) 
                        json_file.close() 
                        #Had to put this condition becuase the code was pushing single data twice due to app.run thus the "if" condition here
                        if collection.find_one(basename):
                            print("File exists, skipping insertion.")
                        else:
                            pushing = collection.insert_one(basename)
                            print(f"'{os.path.basename(file)}' converted to json and pushed to MongoDB.")
            
                        
                        print(f"'{os.path.basename(file)}'converted to json and pushed to MongoDB.")
                
                #Handlling parsing error if any
                except yaml.YAMLError as yaml_error:
                    print(f"Error config file {os.path.basename(file)}: {yaml_error}")

                #Handelling any other kind of error
                except Exception as e:
                    print(f"Error processing {os.path.basename(file)}: {e}")
                    

        else:
            print("No YAML configuration files were found.")
            
                
    except Exception as e:
        print(f"Error found{e}")

if __name__ == '__main__':
    #Calling the insert function to push the data to MongoDB
    insert()
    app.run(debug=True)


