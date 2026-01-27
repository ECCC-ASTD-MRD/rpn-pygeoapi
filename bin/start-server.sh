#!/bin/bash
set -e

project_dir=$(cd -P $(dirname ${BASH_SOURCE[0]})/.. && pwd)


cp ${project_dir}/share/rpn-pygeoapi/example-config.yml ${project_dir}/pygeoapi/example-config.yml

cd ${project_dir}/pygeoapi

export PYGEOAPI_CONFIG=example-config.yml
export PYGEOAPI_OPENAPI=example-openapi.yml

pygeoapi openapi generate $PYGEOAPI_CONFIG --output-file $PYGEOAPI_OPENAPI
pygeoapi serve
