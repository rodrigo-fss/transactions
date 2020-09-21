docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic cash_ins
docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic cash_outs_processed
docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic cash_outs_created
docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic cash_outs_refunded


cat transaction-data/cash_ins.json | jq -cn --stream 'fromstream( inputs|(.[0] |= .[1:]) | select(. != [[]]) )' | docker-compose exec -T broker kafka-console-producer --broker-list localhost:9092 --topic cash_ins
cat transaction-data/cash_outs_processed.json | jq -cn --stream 'fromstream( inputs|(.[0] |= .[1:]) | select(. != [[]]) )' | docker-compose exec -T broker kafka-console-producer --broker-list localhost:9092 --topic cash_outs_processed
cat transaction-data/cash_outs_created.json | jq -cn --stream 'fromstream( inputs|(.[0] |= .[1:]) | select(. != [[]]) )' | docker-compose exec -T broker kafka-console-producer --broker-list localhost:9092 --topic cash_outs_created
cat transaction-data/cash_outs_refunded.json | jq -cn --stream 'fromstream( inputs|(.[0] |= .[1:]) | select(. != [[]]) )' | docker-compose exec -T broker kafka-console-producer --broker-list localhost:9092 --topic cash_outs_refunded
