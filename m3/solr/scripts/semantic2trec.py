#!/usr/bin/env python3

import argparse
import json
import sys


def results_to_trec(results, run_id="run0"):
    """
    Converts search results to TREC format and writes the results to STDOUT.

    Format:
    qid     iter    docno       rank    sim     run_id
    0       Q0      DOC_ID      1       SCORE   RUN_ID

    Arguments:
    - results: List of dictionaries containing document IDs and scores.
    - run_id: Identifier for the experiment or system (default: run0).

    Output:
    - Writes the converted results to STDOUT.
    """
    try:
        # Enumerate through the results and write them in TREC format
        for rank, doc in enumerate(results, start=1):
            doc_id = doc.get("id", "unknown")  # Fallback to 'unknown' if no ID
            score = doc.get("score", 0.0)      # Fallback to 0.0 if no score
            print(f"0 Q0 {doc_id} {rank} {score} {run_id}")

    except KeyError as e:
        print(f"Error: Missing expected key {e} in results.")
        sys.exit(1)


if __name__ == "__main__":
    # Set up argument parsing for command-line interface
    parser = argparse.ArgumentParser(description="Convert search results to TREC format.")

    # Add argument for optional run ID
    parser.add_argument(
        "--run-id",
        type=str,
        default="run0",
        help="Experiment or system identifier (default: run0).",
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Load results from STDIN
    try:
        results = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input. Please provide a valid JSON file.")
        sys.exit(1)

    # Convert results to TREC format and write to STDOUT
    results_to_trec(results, args.run_id)
