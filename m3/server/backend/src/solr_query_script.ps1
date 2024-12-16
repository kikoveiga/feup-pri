param (
    [string]$SOLR_URL,
    [string]$QUERY_JSON
)

# Perform the curl request with a JSON payload
curl -s -X POST $SOLR_URL -H "Content-Type: application/json" -d $QUERY_JSON