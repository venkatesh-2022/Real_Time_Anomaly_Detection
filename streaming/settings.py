#Importing control Libraries to use at Settings module
import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#You can alter the settings based on the demands and resource allocations

DELAY = 0.01
NUM_PARTITIONS = 3
OUTLIERS_GENERATION_PROBABILITY = 0.2
KAFKA_BROKER = "localhost:9092"
TRANSACTIONS_TOPIC = "transactions"
TRANSACTIONS_CONSUMER_GROUP = "transactions"
ANOMALIES_TOPIC = "anomalies"
ANOMALIES_CONSUMER_GROUP = "anomalies"

# SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
SLACK_API_TOKEN = "xoxb-4429977714134-4475936452161-0tv5bJynbaFyJuC1XYB5oNNS"
SLACK_CHANNEL = "anomalies-alerts"
