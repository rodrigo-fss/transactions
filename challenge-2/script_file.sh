docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic cash_outs_created


jq -rc . transaction-data/cash_outs_created.json | docker-compose exec -T broker kafka-console-producer --broker-list localhost:9092 --topic cash_outs_created

