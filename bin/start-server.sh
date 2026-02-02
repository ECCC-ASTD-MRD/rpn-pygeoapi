#!/bin/bash

set -e

project_dir=$(cd -P $(dirname ${BASH_SOURCE[0]})/.. && pwd)

mkdir ${project_dir}/pygeoapi/tests/data/combined_jsons

cp -r ${project_dir}/combined_jsons ${project_dir}/pygeoapi/tests/data/combined_jsons

cp ${project_dir}/share/rpn-pygeoapi/xarray-custom.py ${project_dir}/pygeoapi/pygeoapi/provider/xarray-custom.py

cp ${project_dir}/share/rpn-pygeoapi/example-config.yml ${project_dir}/pygeoapi/example-config.yml

cd ${project_dir}/pygeoapi

export PYGEOAPI_CONFIG=example-config.yml
export PYGEOAPI_OPENAPI=example-openapi.yml

pygeoapi openapi generate $PYGEOAPI_CONFIG --output-file $PYGEOAPI_OPENAPI
pygeoapi serve
