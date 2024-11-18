#!/bin/bash

# Base directory (parent of the scripts directory)
BASE_DIR="$(dirname "$(realpath "$0")")/.."

# Path to the queries directory
QUERIES_DIR="$BASE_DIR/queries"

# Path to solr2trec.py script
SOLR2TREC_SCRIPT="$BASE_DIR/scripts/solr2trec.py"

# Ensure solr2trec.py exists
if [[ ! -f "$SOLR2TREC_SCRIPT" ]]; then
    echo "Error: solr2trec.py script not found at $SOLR2TREC_SCRIPT."
    exit 1
fi

# Process each query folder (q1, q2, ...)
for QUERY_FOLDER in "$QUERIES_DIR"/q*/; do
    echo "Processing folder: $QUERY_FOLDER"

    # Process simple_result.json
    SIMPLE_RESULT="$QUERY_FOLDER/simple_result.json"
    if [[ -f "$SIMPLE_RESULT" ]]; then
        OUTPUT_FILE="$QUERY_FOLDER/simple.trec"
        cat "$SIMPLE_RESULT" | python3 "$SOLR2TREC_SCRIPT" --run-id "simple" > "$OUTPUT_FILE"
        echo "Generated $OUTPUT_FILE"
    else
        echo "Warning: $SIMPLE_RESULT not found. Skipping."
    fi

    # Process updated_result.json
    UPDATED_RESULT="$QUERY_FOLDER/updated_result.json"
    if [[ -f "$UPDATED_RESULT" ]]; then
        OUTPUT_FILE="$QUERY_FOLDER/updated.trec"
        cat "$UPDATED_RESULT" | python3 "$SOLR2TREC_SCRIPT" --run-id "updated" > "$OUTPUT_FILE"
        echo "Generated $OUTPUT_FILE"
    else
        echo "Warning: $UPDATED_RESULT not found. Skipping."
    fi
done

echo "All TREC result files generated successfully inside their respective directories!"
