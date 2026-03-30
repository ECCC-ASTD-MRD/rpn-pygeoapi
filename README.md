# RPN pygeoapi

RPN pygeoapi

<a href="docs/architecture/c4.container.png"><img alt="RPN pygeoapi C4 component diagram" src="https://gccode.ssc-spc.gc.ca/msc-ip/msc-ip-api/-/raw/main/docs/architecture/c4.component.png?ref_type=heads" width="800"/></a>

## Deployments

- default: http://localhost:5089
- DEV: TODO

## Setup
```bash
# build image
make build

# run API
make up

# stop API
make down

# inspect logs
make logs
```

## Sample requests

- Landing page: http://localhost:5089
- OpenAPI document (SwaggerUI): http://localhost:5089/openapi
- API collections: http://localhost:5089/openapi

## Code Conventions

* [PEP8](https://www.python.org/dev/peps/pep-0008)

## Bugs and Issues

All bugs, enhancements and issues are managed on [GitLab](https://gitlab.science.gc.ca/RPN-SI/rpn-pygeoapi/-/issues)

## Contact

* [Philippe Carphin](https://gitlab.science.gc.ca/phc001)
* [Ibrahim Boudaouara](https://gitlab.science.gc.ca/ibb000)
* [Tom Kralidis](https://gitlab.science.gc.ca/tok001)
