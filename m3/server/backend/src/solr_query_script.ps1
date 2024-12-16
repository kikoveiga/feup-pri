param (
    [string]$SOLR_URL,
    [string]$QUERY_JSON
)

# Perform the POST request with the JSON payload
$response = Invoke-RestMethod -Uri $SOLR_URL -Method Post -ContentType "application/json" -Body $QUERY_JSON

# Output the response as JSON
$response | ConvertTo-Json -Depth 10
