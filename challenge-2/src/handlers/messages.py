import numpy as np


# function that filters vowels
def filter_topic_in_batch(message, topic):
    if message.topic() == topic:
        return True
    else:
        return False


def get_distinct_topics(messages):
    topic_list = [m.topic() for m in messages]
    x = np.array(topic_list)
    return np.unique(x)
