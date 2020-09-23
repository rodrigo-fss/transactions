
# Challenge 2 - Transaction Pipeline

For the challenge 2 I choose to build an pipeline close to what you have seen in the previous challenge - the streaming one - Just used this application instead of the Kafka Connect block. 

As the application just consume the events, it doesn't apply any validation on the data - like if there's balance left on the account to make the cash out - I choose to built a consumer that listen to all the topics, consume messages in chunks, 500 messages per call, and inserts them into the BigQuery - I tested consuming and inserting into the database one message at a time and the performance was far from ok. (BigQuery was used mainly because it's [streaming buffer](https://cloud.google.com/bigquery/streaming-data-into-bigquery) and columnar based architecture - no index management was needed. Redshift or postgres could be used as well).  

I recommend accessing the metabase instance first - so you can check that there isn't any data on the database before the application goes live. You should be able to access the dashboard in [this link](http://34.72.214.45/public/dashboard/6fd49876-5781-425e-9d4d-38e47484445e)

## Running the project
jq package is needed (to transform a list of jsons into a one json per line without ), you can install it on ubuntu with the following commands
#### Dependencies
on MacOS:
```
brew install jq
```
on Ubuntu:
```
sudo apt-get update
sudo apt-get install jq
```
### Running the project
Once you have the dashboard loaded and jq installed just run the following command and watch the pipeline working:

    source create_topics_and_publish.sh

This file brings up all the containers (Kafka Broker, Zookeper, Metabase and the consumer itself), creates the topics and extract the data from json files.

Once the topics are populated the consumer ingest them and by the time the script finish running - or a few seconds latter - the metabase dashboard should already be able to provide all the requested metrics.
  

## Project structure

You can check all the code behind the solution in the `src/` folder.
The consumer entrypoint is in the `consumer/consumer.py`.
You can follow the execution and understand a little bit more of how the solution was built in the files inline comments.

  

---

  

*Disclaimer: the credentials file is only commited to the repository so you can run it locally without any problem. Wouldn't do that in corporative solutions*

  

### Any doubts? Open a github issue or email me - I will be happy to answer you shortly!
