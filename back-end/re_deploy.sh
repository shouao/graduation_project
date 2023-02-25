docker stop $(docker ps -a -q --filter ancestor=back-end --format="{{.ID}}")
docker rm $(docker ps -a -q --filter ancestor=back-end --format="{{.ID}}")
docker rmi back-end

docker build -t back-end .
docker run -d -p 4396:4396 back-end