#!/bin/bash
# @author : Courroux
STARTTIME=$(date +%s)
echo ''
echo 'BEGIN'
echo '1/8 Docker clear'
docker stop courroux-sapp
docker rm --force courroux-sapp
# docker images | grep none | awk '{ print $3; }' | xargs docker rmi --force
docker rmi courroux-sapp:0.0.1 --force
echo '2/8 Angular build prod'
ng build -c production --delete-output-path
echo '3/8 Docker build'
# docker build --pull --rm -f "Dockerfile" -t courroux-sapp:0.0.1 "."
docker build -t courroux-sapp:0.0.1 .
echo '4/8 Docker run'
docker run -d --name courroux-sapp courroux-sapp:0.0.1
echo '5/8 Docker commit'
docker commit courroux-sapp courroux-sapp:0.0.1
echo '6/8 Docker save'
docker save courroux-sapp:0.0.1 > dist/courroux-sapp.tar
# echo '7/8 Docker remove old images'
# docker images | grep none | awk '{ print $3; }' | xargs docker rmi --force
echo '8/8 Docker stop new service and remove it'
docker stop courroux-sapp
docker rm courroux-sapp
echo 'END'
ENDTIME=$(date +%s)
DURATION="$(($ENDTIME - $STARTTIME))"
echo ''
echo '-----------------------------------------------------'
printf ' Script duration: %d minutes %d seconds\n' $((DURATION%3600/60)) $((DURATION%60))
echo '-----------------------------------------------------'
echo ''
