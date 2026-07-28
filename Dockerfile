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

FROM ubuntu:noble

# Define build arguments and environment variables
ARG PYGEOAPI_GITREPO=https://github.com/geopython/pygeoapi.git \
    MSC_PYGEOAPI_GITREPO=https://github.com/ECCC-MSC/msc-pygeoapi.git

ENV BASEDIR=/apps/rpn-pygeoapi-nightly
ENV PROVIDER_DIR=${BASEDIR}/pygeoapi/pygeoapi/provider/
WORKDIR ${BASEDIR}

#RUN sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//mirror:\/\/mirrors.ubuntu.com\/mirrors.txt/g' /etc/apt/sources.list

# Update sources and install system dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:ubuntugis/ubuntugis-unstable && \
    apt-get update && \
    apt-get install -y python3 git curl unzip python3-gdal libgdal-dev python3-pip  python3.12-venv

RUN python3 -m venv ${BASEDIR}/venv

# Clone pygeoapi and install Python dependencies
RUN git clone ${PYGEOAPI_GITREPO} -b master --depth=1 && \
    cd pygeoapi && \
    ${BASEDIR}/venv/bin/pip3 install -r requirements.txt && \
    ${BASEDIR}/venv/bin/pip3 install pip -U && \
    ${BASEDIR}/venv/bin/pip3 install setuptools  && \
    ${BASEDIR}/venv/bin/pip3 install flask_cors aiofiles starlette uvicorn[standard] fsspec kerchunk && \
    ${BASEDIR}/venv/bin/pip3 install . && \
    cd ${BASEDIR}

# Clone msc-pygeoapi and install dependencies
RUN git clone ${MSC_PYGEOAPI_GITREPO} -b master --depth=1 && \
    cd msc-pygeoapi && \
    # Download and configure GCWeb theme
    curl -L https://github.com/wet-boew/GCWeb/releases/download/v14.6.0/themes-dist-14.6.0-gcweb.1.zip -o ./themes-gcweb.zip && \
    unzip -o ./themes-gcweb.zip "*/GCWeb/*" -d theme/static && \
    unzip -o ./themes-gcweb.zip "*/wet-boew/*" -d theme/static && \
    mv ./theme/static/themes-dist-14.6.0-gcweb ./theme/static/themes-gcweb && \
    rm -f ./themes-gcweb.zip && \
    ${BASEDIR}/venv/bin/pip3 install . && \
    # show version of msc-pygeoapi
    MSC_PYGEOAPI_VERSION=$(dpkg-parsechangelog -SVersion) && \
    sed -i "s/MSC_PYGEOAPI_VERSION/$MSC_PYGEOAPI_VERSION/" theme/templates/_base.html && \
    # ensure i18n translation strings are compiled
    ${BASEDIR}/venv/bin/pybabel compile -d locale -l fr && \
    cd ..

# Download schemas for OGC API and clean up unnecessary packages/files
RUN mkdir schemas.opengis.net && \
    curl -O http://schemas.opengis.net/SCHEMAS_OPENGIS_NET.zip && \
    unzip SCHEMAS_OPENGIS_NET.zip "ogcapi/*" -d ${BASEDIR}/schemas.opengis.net && \
    rm -f SCHEMAS_OPENGIS_NET.zip && \
    apt-get remove --purge -y curl unzip && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy application configuration and entrypoint script
COPY ./docker/rpn-pygeoapi-config.yml ${BASEDIR}/rpn-pygeoapi-config.yml
COPY ./docker/entrypoint.sh ${BASEDIR}/entrypoint.sh
COPY ./providers/*.py ${BASEDIR}/venv/lib/python3.12/site-packages/pygeoapi/provider

# Set permission and entrypoint
RUN chmod +x ${BASEDIR}/entrypoint.sh
RUN chmod -R g=u ${BASEDIR}
ENTRYPOINT [ "sh", "-c", "${BASEDIR}/entrypoint.sh" ]
