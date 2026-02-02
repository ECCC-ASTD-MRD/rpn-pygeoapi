#!/bin/bash

if ! (return 0 2>/dev/null) ; then
    echo "Error: This script must be sourced."
    exit 1
fi

ROOT_DIR=$(cd -P $(dirname ${BASH_SOURCE[0]}) && pwd)
VENV_PATH=${ROOT_DIR}/venv/bin/activate

if [ ! -f "${VENV_PATH}" ] ; then
    echo "Error: 'venv' not found"
    return 1
fi

source ${VENV_PATH}
