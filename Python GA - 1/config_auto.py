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
#Importing MongoClient for the interaction with MongoDB
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
        #Declaring an empty list
        yaml_list = []
        
        #Parsing through the response we got from MongoDB
        for element in configuartions:
             
             print("********************************")
             print(element["filename"])
             print(element)
             get_request = json_util.dumps(element)
             #Converting the json-string to dict
             json_to_dict = json_util.loads(get_request)
             #Converting the dict to yaml string
             yaml_data = yaml.dump(json_to_dict, default_flow_style=False)
             #Appending the loop iterations of each file to a list
             yaml_list.append(yaml_data)
             
        #Returning the list as an output of the get mehtod
        return jsonify(yaml_list)

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
                        #Mapping the filename to the configuration file to let people know which config file they are looking at
                        yaml_dict["filename"] = os.path.basename(file)
                        yaml_to_json = json.dumps(yaml_dict, indent=1)
                        print(yaml_to_json)
                        #creating json and writing to it.
                        json_file = open(f"{os.path.basename(file)}.json", "w")  
                        json_file.write(yaml_to_json) 
                        json_file.close() 
                        #Had to put this condition becuase the code was pushing single data twice due to app.run thus the "if" condition here
                        if collection.find_one(yaml_dict):
                            print("File exists, skipping insertion.")
                        else:
                            pushing = collection.insert_one(yaml_dict)
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


