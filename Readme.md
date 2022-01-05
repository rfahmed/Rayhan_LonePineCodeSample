# Docs - Lone Pine Coding Sample:
## Usage: 
To execute the program simply run the ingest_file.py python script.
This can be done by executing '$python3 ingest_file.py'
## Dependencies:
The program has 7 dependencies:
##### AWS Configure: 
You need to run '$aws configure' from the command line before executing the program.
Instructions: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
##### Boto3: 
Install the python package boto3: '$pip3 install boto3'
##### datetime: 
Install the python package datetime: '$pip3 install datetime'
##### os: 
Ensure you have access to the os library (should be included with python by default)
##### apscheduler.schedulers.blocking: 
Install the python package apscheduler: '$pip3 install apscheduler'
##### warnings:
Ensure you have access to the warnings library (should be included with python by default)
##### pandas: 
Install the python package pandas: '$pip3 install pandas'
#### File System:
Ensure you have a directory in your program titled cached_data/
## Answering Future Questions:
The questions provided were very specific to certain states, years, features in the data, etc. 
To ensure that this code is able to handle future questions that may arise along the same lines I
tried to make the functions as versitile as possible. For the state/year functions I allowed the user
to pick any state/year and any feature in the data. I also wrote about how these functions could be 
adapted for even wider scope in the function descriptions. The code provided here covers the major 
tasks in this dataset of slicing, getting value counts by various features, and converting the data
to a datetime model which allows us to easily preform time series operations on it. Through all of these
methods I think any future development team would have an easy time adapting this script for other use cases.
