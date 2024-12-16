#!/bin/bash

SOLR_URL=$1
QUERY_JSON=$2

# Perform the curl request with a JSON payload
curl -s -X POST "${SOLR_URL}" -H "Content-Type: application/json" -d "${QUERY_JSON}"
