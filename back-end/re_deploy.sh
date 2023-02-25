docker stop $(sudo docker ps -a -q --filter ancestor=back-end --format="{{.ID}}")
docker rm $(sudo docker ps -a -q --filter ancestor=back-end --format="{{.ID}}")
docker rmi back-end

docker build -t back-end .
docker run -d --network host back-end