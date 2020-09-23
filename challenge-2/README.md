# Challenge 2 - Transaction Pipeline

For the challenge 2 I choose to build an pipeline close to what you have seen in the previous challenge - the streaming pipeline - Just used this application instead of Kafka Connect.

As the application just consume the events, it doesn't apply any validation or transformation on the data - like if there's balance left on the account to make the cash out - I choose to build a consumer that listen to all the topics, consume messages in chunks, 500 messages per call, and inserts them into BigQuery - I tested consuming and inserting into the database one message at a time and the performance was far from ok. (BigQuery was used mainly because it's [streaming buffer](https://cloud.google.com/bigquery/streaming-data-into-bigquery) and columnar based architecture - no index management was needed. Redshift or postgres could be used as well).

I recommend accessing the metabase instance first - so you can check that there isn't any data on the database before the application goes live. You should be able to access the dashboard in [this link](http://34.72.214.45/public/dashboard/6fd49876-5781-425e-9d4d-38e47484445e)

**If you run the application more than once the events will be duplicated**. I'd like to truncate the table before each run but bigquerys streaming buffer only persists the messages after a period of time and till that happens inserts cant be deleted. As data is almost never deleted in production I thought it would be ok.

**My suggestion is to check the correctness of the answer in the first run and than running it as needed to check performance - I inserted a few hundred thousand rows and the solution kept working beautifully**

## Running the project

#### Dependencies

jq package is needed (to transform a list of jsons into a one json per line without any code), you can install it on ubuntu or macos with the following commands

on MacOS: `brew install jq`

on Ubuntu:

```

sudo apt-get update

sudo apt-get install jq

```
[docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) are also needed!

### Running the project

Once you have the dashboard loaded and jq installed just run the following command and watch the pipeline working:

    source create_topics_and_publish.sh

This file brings up all the containers (Kafka Broker, Zookeper, Metabase and the consumer itself), creates the topics and extract the data from json files.

Once the topics are populated the consumer ingest them and by the time the script finish running - or a few seconds latter - the metabase dashboard should already be able to provide all the requested metrics.

### Re-Running the application
To stop the application - the correct way - so you can put it back up, please use the following command `docker-compose down --remove-orphans` on the root of this challenge.

After all containers have stopped you are good to put it back up with `source create_topics_and_publish.sh` again!
## Project structure

You can check all the code behind the solution in the `src/` folder.

The consumer entrypoint is in the `consumer/consumer.py`.

You can follow the execution and understand a little bit more of how the consumer was built in the files inline comments.

---
 
*Disclaimer: the credentials file is only commited to the repository so you can run it locally without any problem. Wouldn't do that in corporative solutions*

### Any doubts? Open a github issue or email me - I will be happy to answer you shortly!
