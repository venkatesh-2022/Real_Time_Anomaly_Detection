#Importing Libs to use here
import json
import os
from joblib import load
import logging
from multiprocessing import Process

import numpy as np
import calendar
import time


# import sys
# from pathlib import Path
# sys.path[0] = str(Path(sys.path[0]).parent)
from settings import TRANSACTIONS_TOPIC, TRANSACTIONS_CONSUMER_GROUP, ANOMALIES_TOPIC, NUM_PARTITIONS
#trail
#Importing Libs to use here
import logging
import socket

from confluent_kafka import Producer, Consumer

import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)
from settings import KAFKA_BROKER

def create_producer():
    try:
        producer = Producer({"bootstrap.servers": KAFKA_BROKER,
                             "client.id": socket.gethostname(),
                             "enable.idempotence": True,  # EOS processing
                             "compression.type": "lz4",
                             "batch.size": 64000,
                             "linger.ms": 10,
                             "acks": "all",  # Wait for the leader and all ISR to send response back
                             "retries": 5,
                             "delivery.timeout.ms": 1000})  # Total time to make retries
    except Exception as e:
        logging.exception("Couldn't create the producer")
        producer = None
    return producer


def create_consumer(topic, group_id):
    try:
        consumer = Consumer({"bootstrap.servers": KAFKA_BROKER,
                             "group.id": group_id,
                             "client.id": socket.gethostname(),
                             "isolation.level": "read_committed",
                             "default.topic.config": {"auto.offset.reset": "latest", # Only consume new messages
                                                      "enable.auto.commit": False}
                             })

        consumer.subscribe([topic])
    except Exception as e:
        logging.exception("Couldn't create the consumer")
        consumer = None

    return consumer


# import sys
# from pathlib import Path
# sys.path[0] = str(Path(sys.path[0]).parent)
# from streaming.utils import create_producer, create_consumer

model_path = os.path.abspath('isolation_forest.joblib')


def detect():
    consumer = create_consumer(topic=TRANSACTIONS_TOPIC, group_id=TRANSACTIONS_CONSUMER_GROUP)

    producer = create_producer()

    clf = load(model_path)

    count = 0
    Accuracy_Scores_Average = 0
    Time_before_in_ms = int(round(time.time() * 1000))

#Binary loop
    while True:
        message = consumer.poll(timeout=50)
        if message is None:
            continue
        if message.error():
            logging.error("Consumer error: {}".format(message.error()))
            continue

        # Message that came from producer
        record = json.loads(message.value().decode('utf-8'))
        data = record["data"]

        prediction = clf.predict(data)

        # If an anomaly comes in, send it to anomalies topic
        if prediction[0] == -1:
            score = clf.score_samples(data)
            record["score"] = np.round(score, 3).tolist()
            
        
            count += 1
            # print(count)
            Accuracy_Scores_Average += np.round(score, 3)
            if count == 1000:
                Time_after_in_ms = int(round(time.time() * 1000))
                Accuracy_Scores_Average = Accuracy_Scores_Average/count
                Accuracy_Scores_Average = Accuracy_Scores_Average * -100
                print("The average accuracy score for 1000 anomalies is:", Accuracy_Scores_Average)
                print("Time taken to detect 1000 anomalies is: ", (Time_after_in_ms - Time_before_in_ms)/1000, "Seconds")
                print("Time taken to detect 1000 anomalies is: ", ((Time_after_in_ms - Time_before_in_ms)/1000)/60, "Minutes")
                break

            _id = str(record["id"])
            record = json.dumps(record).encode("utf-8")

            producer.produce(topic=ANOMALIES_TOPIC,
                             value=record)
            producer.flush()
            
        consumer.commit() # comment to process a few messages, not just new ones
    consumer.close()


# One consumer per partition
if __name__ == '__main__':
 for _ in range(NUM_PARTITIONS):
    p = Process(target=detect)
    p.start()
