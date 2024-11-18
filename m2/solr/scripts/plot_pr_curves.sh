#!/bin/bash

# Base directory (parent of the scripts directory)
BASE_DIR="$(dirname "$(realpath "$0")")/.."

# Path to the queries directory
QUERIES_DIR="$BASE_DIR/queries"

# Path to the PR curve Python script
PR_SCRIPT="$BASE_DIR/scripts/plot_pr.py"

# Ensure the PR script exists
if [[ ! -f "$PR_SCRIPT" ]]; then
    echo "Error: PR curve script not found at $PR_SCRIPT."
    exit 1
fi

# Folders to process (q1, q2, q3)
FOLDERS=("q1" "q2" "q3")

# Iterate through each folder
for FOLDER in "${FOLDERS[@]}"; do
    QUERY_FOLDER="$QUERIES_DIR/$FOLDER"
    echo "Processing folder: $QUERY_FOLDER"

    # Ensure qrels.trec exists
    QRELS_FILE="$QUERY_FOLDER/qrels.trec"
    if [[ ! -f "$QRELS_FILE" ]]; then
        echo "Warning: $QRELS_FILE not found. Skipping $FOLDER."
        continue
    fi

    # Process simple.trec
    SIMPLE_FILE="$QUERY_FOLDER/simple.trec"
    if [[ -f "$SIMPLE_FILE" ]]; then
        OUTPUT_FILE="$QUERY_FOLDER/simple_pr.png"
        echo "Generating PR curve for $SIMPLE_FILE -> $OUTPUT_FILE"
        cat "$SIMPLE_FILE" | python3 "$PR_SCRIPT" --qrels "$QRELS_FILE" --output "$OUTPUT_FILE"
    else
        echo "Warning: $SIMPLE_FILE not found in $FOLDER. Skipping."
    fi

    # Process updated.trec
    UPDATED_FILE="$QUERY_FOLDER/updated.trec"
    if [[ -f "$UPDATED_FILE" ]]; then
        OUTPUT_FILE="$QUERY_FOLDER/updated_pr.png"
        echo "Generating PR curve for $UPDATED_FILE -> $OUTPUT_FILE"
        cat "$UPDATED_FILE" | python3 "$PR_SCRIPT" --qrels "$QRELS_FILE" --output "$OUTPUT_FILE"
    else
        echo "Warning: $UPDATED_FILE not found in $FOLDER. Skipping."
    fi
done

echo "All PR curves generated successfully!"
