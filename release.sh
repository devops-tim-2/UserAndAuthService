#!/bin/bash

DOCKERHUB_USERNAME=${1}
DOCKERHUB_PASSWORD=${2}
VERSION=${3}
IMAGE=user

FULL_IMAGE_NAME=${DOCKERHUB_USERNAME}/${IMAGE}:${VERSION}

# build image
DOCKER_BUILDKIT=1 docker build -t "${FULL_IMAGE_NAME}" --no-cache .
# login to docker hub
docker login -u=${DOCKERHUB_USERNAME} -p=${DOCKERHUB_PASSWORD}
# push it
docker push "${FULL_IMAGE_NAME}"
