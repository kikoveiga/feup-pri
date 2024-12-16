# Makefile
SHELL := /bin/bash

.PHONY: help
help:
	@echo "Commands:"
	@echo "style      : runs style formatting."
	@echo "down       : stops all running services, removes containers and volumes."
	@echo "up         : start Docker daemon and Solr."
	@echo "schema     : update schema using docker/data/schema.json."
	@echo "populate   : populate Solr using docker/data/data.json."
	@echo "trec_eval  : download trec_eval source code and compile it."
	@echo "test       : run unit tests."

.PHONY: style
style:
	isort src test --atomic
	black -l 100 src test
	flake8 src test

.PHONY: down
down:
	docker compose -f docker/docker-compose.yml down --remove-orphans -v

.PHONY: up
up:
	docker compose -f docker/docker-compose.yml up -d

.PHONY: schema_simple
schema_simple:
	curl -X POST \
		-H 'Content-type:application/json' \
		--data-binary "@./docker/data/schema_simple.json" \
		http://localhost:8983/solr/monuments/schema

.PHONY: schema_updated
schema_updated:
	curl -X POST \
		-H 'Content-type:application/json' \
		--data-binary "@./docker/data/schema_updated.json" \
		http://localhost:8983/solr/monuments/schema

.PHONY: populate
populate:
	docker exec -it monuments bin/solr post -c monuments /data/data.json

.PHONY: generate_embeddings
generate_embeddings:
	python3 scripts/get_embeddings.py < docker/data/data.json > docker/data/semantic_data.json

.PHONY: populate_semantic
populate_semantic:
	docker exec -it monuments bin/solr post -c monuments /data/semantic_data.json

.PHONY: semantic_query
semantic_query:
	python3 scripts/query_embedding.py

.PHONY: trec_eval
trec_eval:
	git clone https://github.com/usnistgov/trec_eval.git src/trec_eval
	cd src/trec_eval && make
	cd ../..

.PHONY: test
test:
	python3 -m unittest discover -s test -p 'test_*.py'
