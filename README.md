# **Онлайн кинотеатр**

## ***Процесс запуска приложения***

### 1. Создать файлы .env по *.env.example

1. Для контейнеров приложения в ./env
2. Для сервис аналитики в ./analytics-collector
3. Для сервис выдачи контента в ./api
4. Для сервис авторизации в ./auth-service
5. Для сервис администратора в ./django-admin
6. Для ETL
    - ./etl_kafka_to_ch
    - ./etl_kafka_to_mongo
    - ./etl_postgres_to_es
7. Для сервиса продюсера кафки в ./kafka-producer
8. Для UGC сервиса в ./ugc-service
9. Для workers кафки
    - ./worker_notification
    - worker_sender

### 2. Запуск контейнеров

``` sh
docker compose up -d
```

### 3. Настройка кластера MongoDB

- Для начала настроим серверы конфигурации.

```sh
docker exec Mongo-Config-1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh' 
```

- Можно проверить статус, выполнив команду на первом сервере конфигурации.

```sh
docker exec Mongo-Config-1 bash -c 'echo "rs.status()" | mongosh' 
```

- Далее, соберём набор реплик первого шарда.

```sh
docker exec MongoDB-Shard1-Node1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh' 
```

- Теперь ноды шарда знают друг друга. Один из них стал первичным (primary), а два других — вторичными (secondary). Вы можете проверить статус реплик с помощью такой команды:

```sh
docker exec MongoDB-Shard1-Node1 bash -c 'echo "rs.status()" | mongosh' 
```

- Наконец, познакомим шард с маршрутизаторами.

```sh
docker exec MongoRouter-1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
```

- Второй шард добавим по аналогии. Сначала инициализируем реплики.

```sh
docker exec MongoDB-Shard2-Node1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh' 
```

- Затем добавим их в кластер.

```sh
docker exec MongoRouter-1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh' 
```

- Теперь маршрутизаторы-интерфейсы кластера для клиентов знают о существовании шардов. Можно проверить статус с помощью команды, запущенной на первом маршрутизаторе.

```sh
docker exec MongoRouter-1 bash -c 'echo "sh.status()" | mongosh'
```

### 4. Создать миграции БД

- Сервис авторизации

``` sh
docker exec Auth bash -c 'alembic upgrade head'
```

- Сервис профиля

``` sh
docker exec Profile bash -c 'alembic upgrade head'
```

- Сервис администратора

``` sh
docker exec Admin bash -c 'python manage.py migrate'
```

### 5. Создать администратора и его право

``` sh
docker exec Auth bash -c 'python admin_init.py create-admin --name Jack --password whoknows --email jack@gmail.com'
```

## ***Ручки приложения***

1. Сервис администратора
    - <http://localhost:81/>

2. Сервис аналитики
    - <http://localhost:82/>

3. Cервис выдачи контента
    - <http://localhost:80/>

4. Cервис авторизации
    - <http://localhost:90/>

5. Jaeger
    - <http://localhost:93/>

6. Kafka
    - <http://localhost:92/>

7. Kibana
    - <http://localhost:94/>

8. UGC
    - <http://localhost:91/>

9. Profile
    - <http://localhost:83/>

## ***Запуск тестов***

``` sh
cd ./tests/functional
```

<ins>Создать файлы .env по ./env/*.env.example </ins>

``` sh
docker compose up -d
./entrypoint_mongo.sh
docker restart Profile_test UGC_test
./run_tests.sh
```
