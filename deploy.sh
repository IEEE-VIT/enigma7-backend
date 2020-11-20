# !/bin/bash
for container_id in `docker ps --format "table {{.ID}}  {{.Names}}  {{.CreatedAt}}" | grep web | awk -F  "  " '{print $1}'`
do
    container_ids+=($container_id)
done
docker-compose up -d --build --no-deps --scale web=6 --no-recreate web
sleep 10
for container_id in "${container_ids[@]}"
do
    docker kill -s SIGTERM $container_id
done
sleep 1
for container_id in "${container_ids[@]}"
do
    docker rm -f $container_id
done
sleep 1
docker-compose up -d --no-deps --scale web=3 --no-recreate web
