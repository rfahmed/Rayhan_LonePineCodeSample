# Name: Rayhan Ahmed
# Date: 1/5/22
# Lone Pine Code Sample
import boto3  # AWS's python SDK, requires you to run 'aws configure' on the cli prior to use
from datetime import date  # Get date info for string formatting
import os  # to check file paths
from apscheduler.schedulers.blocking import BlockingScheduler  # to run this job every minute
import warnings

import analysis_questions  # analysis file we wrote


def main():
    """
    function: main
    params: N/a
    use: drives s3 file download and calls analysis on new data
    """
    current_date = date.today()
    formatted_date_str = current_date.strftime("%Y%m%d")

    formatted_date_str = 20211109  # using date from instructions for sample, delete this to use the current date (prod)

    full_filename = f'vehicle_data_sample_{formatted_date_str}.csv.gz'

    if not os.path.exists(f'cached_data/{full_filename}'):  # check if file is already in our cache
        print(f'Downloading New File: {full_filename} ...')
        s3client = boto3.client('s3')  # create an s3 client, Note: Requires you are logged in on the aws cli
        s3client.download_file('lpc-pub', full_filename, f'cached_data/{full_filename}')  # grab file
    else:
        print(f'File {full_filename} already present in cached data, moving on to analysis...')

    analysis_questions.driver(full_filename)


main()  # We should run our script right now and then schedule it for the next day (otherwise we wait a day at onset)
warnings.filterwarnings(
    "ignore")  # ignore time zone warnings for now (they make our output messy). TODO: Set time zones
scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', days=1)  # run the script every day
scheduler.start()

'''
General thoughts:
- this auth process would be easier if we made a presigned URL, that way we could use a get request instead of boto3.
    - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
- there are many options for running this script every day, I chose to use apscheduler as it can be executed from within
  the script as opposed to Cron which needs to be run from the command line and is only on a unix os
- There was nothing stated in the instructions about storing our analysis data so I assumed that writing the functions
  was enough as this data is probably going to a deployed service/pipeline as opposed to being stored locally. 
- We could also probably make this workflow much easier by running a script on these daily CSVs to upload them to a 
  time series database or another database and run this standard analysis as a set of queries every day
  - This also makes it very easy to add/delete and track query results over time within a sql console 
'''
