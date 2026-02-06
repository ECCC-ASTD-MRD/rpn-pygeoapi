#!/bin/bash

set -e

project_dir=$(cd -P $(dirname ${BASH_SOURCE[0]})/.. && pwd)

export PYTHONPATH=$PYTHONPATH:${project_dir}/share/rpn-pygeoapi # to access custom providers

export PYGEOAPI_CONFIG=${project_dir}/share/rpn-pygeoapi/example-config.yml
export PYGEOAPI_OPENAPI=example-openapi.yml

pygeoapi openapi generate $PYGEOAPI_CONFIG --output-file $PYGEOAPI_OPENAPI
pygeoapi serve
