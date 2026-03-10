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

DOCKER_COMPOSE_ARGS=--file docker/docker-compose.yml --file docker/docker-compose.override.yml --project-name rpn-pygeoapi

build:
	docker compose $(DOCKER_COMPOSE_ARGS) build

up:
	docker compose $(DOCKER_COMPOSE_ARGS) up -d

down:
	docker compose $(DOCKER_COMPOSE_ARGS) down

restart: down up

login:
	docker exec -ti rpn-pygeoapi /bin/bash

force-build:
	docker compose $(DOCKER_COMPOSE_ARGS) build --no-cache

logs:
	docker compose $(DOCKER_COMPOSE_ARGS) logs -f

.PHONY: build up down restart force-build logs
