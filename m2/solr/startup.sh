#!/bin/bash

# This script expects a container started with the following command.
sudo docker run -p 8983:8983 --name monuments -v ${PWD}:/data -d solr:9 solr-precreate monuments

sleep 4

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@schema_updated.json" \
    http://localhost:8983/solr/monuments/schema

# Populate collection using mapped path inside container.
sudo docker exec -it monuments bin/post -c monuments /data/data.json
