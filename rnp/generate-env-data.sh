#!/bin/bash
# Generate a data file with all environment variable names
# This should be run before Hugo builds the site

set -e

OUTPUT_FILE="data/envvars.json"

# Create data directory if it doesn't exist
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Generate JSON with all environment variable names
echo '{"allVars":' > "$OUTPUT_FILE"
env | awk -F= '{print $1}' | sort | jq -R . | jq -s . >> "$OUTPUT_FILE"
echo '}' >> "$OUTPUT_FILE"

echo "Generated $OUTPUT_FILE with $(env | wc -l) environment variables"
