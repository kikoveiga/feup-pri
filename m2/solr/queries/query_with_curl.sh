#!/bin/bash

# Usage: bash query_with_curl.sh <schema_type>
SCHEMA_TYPE=$1

# Validate input
if [[ "$SCHEMA_TYPE" != "simple" && "$SCHEMA_TYPE" != "updated" ]]; then
    echo "Error: Invalid schema type. Use 'simple' or 'updated'."
    exit 1
fi

# Directories for queries and results
BASE_DIR=".."
QUERY_DIR="$BASE_DIR/queries_$SCHEMA_TYPE"
RESULTS_DIR="$BASE_DIR/results_$SCHEMA_TYPE"

# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"

# Solr configuration
SOLR_URI="http://localhost:8983/solr"
COLLECTION="monuments"

# Iterate through all JSON query files in QUERY_DIR
for query_file in "$QUERY_DIR"/*.json; do
    # Extract the base name (e.g., "query1.json" -> "query1")
    query_name=$(basename "$query_file" .json)
    result_file="$RESULTS_DIR/${query_name}_results.json"

    echo "Processing query: $query_name"

    # Execute the curl command
    curl -s -X POST -H "Content-Type: application/json" \
        --data-binary "@$query_file" \
        "$SOLR_URI/$COLLECTION/select" > "$result_file"

    echo "Results saved to: $result_file"
done

echo "All queries processed. Results are in the $RESULTS_DIR directory."
