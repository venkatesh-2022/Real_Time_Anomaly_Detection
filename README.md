# Real_Time_Anomaly_Detection
Project for real-time anomaly detection using kafka and python

Intially, you should have kafka and zookeeper up and running.

Please run these commands in cmd going into folder where you installed kafka.
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
.\bin\windows\kafka-server-start.bat .\config\server.properties

You can follow these steps going forward:
STEP 1:Train an unsupervised machine learning model for anomalies detection task. Pickle/Save the model to be used in real-time predictions. Run train.py for this.
STEP2: Create two topics transaction and anomalies. Run below to commands from cmd going to windows folder in kafka.
        kafka-topics.bat --create --topic transactions --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3
        kafka-topics.bat --create --topic anomalies --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3
STEP 3. Generate fake streaming data and send it to a kafka topic. Run producer.py for this. To check data flow run below command in cmd.
       kafka-console-consumer.bat --bootstrap-server 127.0.0.1:9092 --topic transactions 
STEP 4. Read the topic data with several subscribers to be analyzed by the model. Run anomalies_detector.py file simultaneously after producer.py
        kafka-console-consumer.bat --bootstrap-server 127.0.0.1:9092 --topic anomalies
STEP 5. Predict if the data is an anomaly, if so, send the data to another kafka topic. Run bot_alerts.py for this.
STEP 6. Create a slack app, create a slack channel configure it with code in settings.py and bot_alerts.py.
