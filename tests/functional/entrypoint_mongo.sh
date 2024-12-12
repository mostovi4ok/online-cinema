echo
echo 'sleep 5'
sleep 5

docker exec Mongo-Config-1_test bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'

echo
echo 'sleep 5'
sleep 5

docker exec MongoDB-Shard1-Node1_test bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'

echo
echo 'sleep 5'
sleep 5

docker exec MongoRouter-1_test bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'

echo
echo 'sleep 5'
sleep 5

docker exec MongoDB-Shard2-Node1_test bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'

echo
echo 'sleep 5'
sleep 5

docker exec MongoRouter-1_test bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'

echo
echo 'sleep 5'
sleep 5
