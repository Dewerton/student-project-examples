#!/usr/bin/env bash
set -e

echo -e "\n---Getting job-launcher name & version---"
NAME="$(python setup.py --name)"
VERSION="$(python setup.py --version)"
echo "NAME: $NAME"
echo "VERSION: $VERSION"

TAG="${NAME}:$VERSION"
echo -e "\n---Building ${TAG} docker image---"
docker build --tag "$TAG" .

echo -e "\n---Creating the latest docker image---"
docker tag "$TAG" "${NAME}:latest"