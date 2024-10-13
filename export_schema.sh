#!/bin/bash

# Load environment variables from .env file
set -o allexport
source .env
set -o allexport

# Use the DB_FILE from the .env file
TEXT_FILE="schema.txt"
SCHEMA_FOLDER="output/$DB_FILE"
mkdir -p $SCHEMA_FOLDER
SCHEMA_OUTPUT="$SCHEMA_FOLDER/$TEXT_FILE"
echo $SCHEMA_OUTPUT

# Export the schema
sqlite3 "$DB_FILE" <<EOF
.output $SCHEMA_OUTPUT
.schema
.output
EOF

echo "Schema has been exported to $SCHEMA_OUTPUT"
