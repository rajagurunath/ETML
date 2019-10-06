cd /workspace/ETML/kafka_tars/kafka_2.12-2.3.0

#start zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties &

#start kafka server
bin/kafka-server-start.sh config/server.properties &


