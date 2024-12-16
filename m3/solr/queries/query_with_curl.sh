#!/bin/bash

# Usage: bash queries/query_with_curl.sh <schema_type>
SCHEMA_TYPE=$1

# Validate input
if [[ "$SCHEMA_TYPE" != "simple" && "$SCHEMA_TYPE" != "updated" ]]; then
    echo "Error: Invalid schema type. Use 'simple' or 'updated'."
    exit 1
fi

# Solr configuration
SOLR_URI="http://localhost:8983/solr"
COLLECTION="monuments"

# Iterate through all query subdirectories (e.g., q1, q2, q3)
for query_dir in queries/*; do
    # Ensure it's a directory
    if [[ -d "$query_dir" ]]; then
        # Locate the specific query file based on schema type
        query_file="$query_dir/$SCHEMA_TYPE.json"
        result_file="$query_dir/${SCHEMA_TYPE}_result.json"

        # Check if the query file exists
        if [[ -f "$query_file" ]]; then
            echo "Processing query in $query_dir using $SCHEMA_TYPE schema..."

            # Execute the curl command
            curl -s -X POST -H "Content-Type: application/json" \
                --data-binary "@$query_file" \
                "$SOLR_URI/$COLLECTION/select" > "$result_file"

            echo "Results saved to: $result_file"
        else
            echo "Query file $query_file does not exist. Skipping $query_dir."
        fi
    fi
done

echo "All queries processed for the $SCHEMA_TYPE schema."
