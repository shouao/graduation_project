docker stop $(docker ps -a -q --filter ancestor=front-end --format="{{.ID}}")
docker rm $(docker ps -a -q --filter ancestor=front-end --format="{{.ID}}")
docker rmi front-end

docker build -t front-end .
docker run -d --network host front-end