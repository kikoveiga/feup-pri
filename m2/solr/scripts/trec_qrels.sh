#!/bin/bash

# Base directory (parent of the scripts directory)
BASE_DIR="$(dirname "$(realpath "$0")")/.."

# Path to the queries directory
QUERIES_DIR="$BASE_DIR/queries"

# Path to qrels2trec.py script
QRELS2TREC_SCRIPT="$BASE_DIR/scripts/qrels2trec.py"

# Ensure qrels2trec.py exists
if [[ ! -f "$QRELS2TREC_SCRIPT" ]]; then
    echo "Error: qrels2trec.py script not found at $QRELS2TREC_SCRIPT."
    exit 1
fi

# Process each query folder (q1, q2, ...)
for QUERY_FOLDER in "$QUERIES_DIR"/q*/; do
    echo "Processing folder: $QUERY_FOLDER"

    # Path to the qrels.txt file
    QRELS_FILE="$QUERY_FOLDER/qrels.txt"
    
    # Check if qrels.txt exists
    if [[ -f "$QRELS_FILE" ]]; then
        # Output file for the converted TREC QREL format
        OUTPUT_FILE="$QUERY_FOLDER/qrels.trec"

        # Convert qrels.txt to TREC format using qrels2trec.py
        cat "$QRELS_FILE" | python3 "$QRELS2TREC_SCRIPT" > "$OUTPUT_FILE"
        echo "Generated $OUTPUT_FILE"
    else
        echo "Warning: $QRELS_FILE not found. Skipping."
    fi
done

echo "All QREL files converted to TREC format successfully!"
