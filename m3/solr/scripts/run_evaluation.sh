#!/bin/bash

# Base directory (parent of the scripts directory)
BASE_DIR="$(dirname "$(realpath "$0")")/.."

# Path to the queries directory
QUERIES_DIR="$BASE_DIR/queries"

# Path to trec_eval executable
TREC_EVAL_EXEC="$BASE_DIR/src/trec_eval/trec_eval"

# Ensure trec_eval exists
if [[ ! -f "$TREC_EVAL_EXEC" ]]; then
    echo "Error: trec_eval executable not found at $TREC_EVAL_EXEC."
    exit 1
fi

# Folders to process (q1, q2, q3)
FOLDERS=("q1" "q2" "q3")

# Iterate through the selected folders
for FOLDER in "${FOLDERS[@]}"; do
    QUERY_FOLDER="$QUERIES_DIR/$FOLDER"
    echo "Processing folder: $QUERY_FOLDER"

    # Ensure qrels.trec exists
    QRELS_FILE="$QUERY_FOLDER/qrels.trec"
    if [[ ! -f "$QRELS_FILE" ]]; then
        echo "Warning: $QRELS_FILE not found. Skipping $FOLDER."
        continue
    fi

    # Evaluate simple.trec
    SIMPLE_FILE="$QUERY_FOLDER/simple.trec"
    if [[ -f "$SIMPLE_FILE" ]]; then
        OUTPUT_FILE="$QUERY_FOLDER/simple_eval.txt"
        echo "Evaluating $SIMPLE_FILE against $QRELS_FILE -> $OUTPUT_FILE"
        "$TREC_EVAL_EXEC" -q "$QRELS_FILE" "$SIMPLE_FILE" > "$OUTPUT_FILE"
    else
        echo "Warning: $SIMPLE_FILE not found in $FOLDER. Skipping."
    fi

    # Evaluate updated.trec
    UPDATED_FILE="$QUERY_FOLDER/updated.trec"
    if [[ -f "$UPDATED_FILE" ]]; then
        OUTPUT_FILE="$QUERY_FOLDER/updated_eval.txt"
        echo "Evaluating $UPDATED_FILE against $QRELS_FILE -> $OUTPUT_FILE"
        "$TREC_EVAL_EXEC" -q "$QRELS_FILE" "$UPDATED_FILE" > "$OUTPUT_FILE"
    else
        echo "Warning: $UPDATED_FILE not found in $FOLDER. Skipping."
    fi
done

echo "All evaluations completed!"
