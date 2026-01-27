#!/bin/bash
set -e

if ! (return 0 2>/dev/null) ; then
    echo "This script must be sourced"
    exit 1
fi

this_dir=$(cd -P $(dirname ${BASH_SOURCE[0]}) && pwd)
source ${this_dir}/venv/bin/activate
