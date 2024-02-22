#!/usr/bin/env bash

full_path=$(realpath $0)
dir_path=$(dirname $full_path)
cd $dir_path

docker build -t his-notifier-build-env .
docker run -i --rm -v $dir_path/../:/app his-notifier-build-env /app/linux_build_env/package.sh
