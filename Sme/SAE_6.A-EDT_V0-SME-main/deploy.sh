#!/bin/bash
# @author : Courroux
STARTTIME=$(date +%s)
echo ''
echo 'BEGIN'
echo '1/7 Docker clear'
docker stop courroux-sme
docker rm --force courroux-sme
docker images | grep none | awk '{ print $3; }' | xargs docker rmi --force
echo '2/7 Docker build'
docker build --pull --rm -f "Dockerfile" -t courroux-sme:0.0.1 "."
echo '3/7 Docker run'
docker run -d --name courroux-sme courroux-sme:0.0.1
echo '4/7 Docker commit'
docker commit courroux-sme courroux-sme:0.0.1
echo '5/7 Docker save'
docker save courroux-sme:0.0.1 > dist/courroux-sme.tar
echo '6/7 Docker remove old images'
docker images | grep none | awk '{ print $3; }' | xargs docker rmi --force
echo '7/7 Docker stop new service and remove it'
docker stop courroux-sme
docker rm courroux-sme
echo 'END'
ENDTIME=$(date +%s)
DURATION="$(($ENDTIME - $STARTTIME))"
echo ''
echo '-----------------------------------------------------'
printf ' Script duration: %d minutes %d seconds\n' $((DURATION%3600/60)) $((DURATION%60))
echo '-----------------------------------------------------'
echo ''
