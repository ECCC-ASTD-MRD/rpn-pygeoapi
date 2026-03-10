#!/bin/bash
###################################################################
#
# Author: Tom Kralidis <tom.kralidis@ec.gc.ca>
#
# Copyright (c) 2026 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
###################################################################

# pygeoapi entry script

echo "START /entrypoint.sh"

set +e

# gunicorn env settings with defaults
SCRIPT_NAME="/"
CONTAINER_NAME="rpn-pygeoapi"
CONTAINER_HOST=${CONTAINER_HOST:=0.0.0.0}
CONTAINER_PORT=${CONTAINER_PORT:=80}
WSGI_WORKERS=${WSGI_WORKERS:=8}

export RPN_PYGEOAPI_TEMPLATES=${RPN_PYGEOAPI_BASEDIR}/msc-pygeoapi/theme/templates
export RPN_PYGEOAPI_STATIC=${RPN_PYGEOAPI_BASEDIR}/msc-pygeoapi/theme/static
export RPN_PYGEOAPI_OGC_SCHEMAS_LOCATION=${RPN_PYGEOAPI_BASEDIR}/schemas.opengis.net

# What to invoke: default is to run gunicorn server
entry_cmd=${1:-run}

# Shorthand (bash)
function error() {
    echo "ERROR: $@"
}

echo "Hotfixing HTML template for landing page and associated text"

sed -i 's/MSC GeoMet User Documentation/MSC Information Pool documentation/' $RPN_PYGEOAPI_BASEDIR/msc-pygeoapi/theme/templates/landing_page.html

cat <<EOF >> $RPN_PYGEOAPI_BASEDIR/msc-pygeoapi/locale/en/LC_MESSAGES/messages.po
msgid "MSC Information Pool documentation"
msgstr ""
EOF

cat <<EOF >> $RPN_PYGEOAPI_BASEDIR/msc-pygeoapi/locale/fr/LC_MESSAGES/messages.po
msgid "MSC Information Pool documentation"
msgstr "Documentation de la plateforme Information Pool du SMC"
EOF


$RPN_PYGEOAPI_BASEDIR/venv/bin/pybabel compile -d $RPN_PYGEOAPI_BASEDIR/msc-pygeoapi/locale -l fr

echo "Trying to generate OpenAPI document with PYGEOAPI_CONFIG=${PYGEOAPI_CONFIG} and PYGEOAPI_OPENAPI=${PYGEOAPI_OPENAPI}..."
$RPN_PYGEOAPI_BASEDIR/venv/bin/pygeoapi openapi generate ${PYGEOAPI_CONFIG} --output-file ${PYGEOAPI_OPENAPI} --no-fail-on-invalid-collection

# Check if the OpenAPI document was generated successfully
if [[ $? -ne 0 || ! -s ${PYGEOAPI_OPENAPI} ]]; then
    error "${PYGEOAPI_OPENAPI} could not be generated or is empty. Exiting gracefully."
    exit 1
    # alternative fallback for testing
    # DEFAULT_PYGEOAPI_OPENAPI=${RPN_PYGEOAPI_BASEDIR}/msc-pygeoapi/deploy/default/msc-pygeoapi-openapi.yml
    # echo "Using default OpenAPI document with DEFAULT_PYGEOAPI_OPENAPI=${DEFAULT_PYGEOAPI_OPENAPI}"
    # cp -f ${DEFAULT_PYGEOAPI_OPENAPI} ${PYGEOAPI_OPENAPI}
    # sed -i "s/MSC_PYGEOAPI_OGC_API_URL/RPN_PYGEOAPI_OGC_API_URL/" ${PYGEOAPI_OPENAPI}
else
    echo "OpenAPI document generated successfully at ${PYGEOAPI_OPENAPI}."
fi

echo "Continuing startup of msc-pygeoapi (${CONTAINER_NAME})..."

case ${entry_cmd} in
    # Run pygeoapi server
    run)
        # SCRIPT_NAME should not have value '/'
        [[ "${SCRIPT_NAME}" = '/' ]] && export SCRIPT_NAME="" && echo "make SCRIPT_NAME empty from /"
        echo "Start uvicorn name=${CONTAINER_NAME} on ${CONTAINER_HOST}:${CONTAINER_PORT} with ${WSGI_WORKERS} workers and SCRIPT_NAME=${SCRIPT_NAME}"
        exec $RPN_PYGEOAPI_BASEDIR/venv/bin/uvicorn \
                --workers ${WSGI_WORKERS} \
                --loop=asyncio \
                --host=${CONTAINER_HOST} \
                --port=${CONTAINER_PORT} \
                pygeoapi.starlette_app:APP \
                --root-path=${RPN_PYGEOAPI_OGC_API_URL_BASEPATH}
      ;;
    *)
      error "unknown command arg: must be 'run'"
      ;;
esac

echo "END /entrypoint.sh"
