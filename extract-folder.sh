#!/bin/bash

# Script to extract a folder from compressed text file
# Usage: ./extract-folder.sh <compressed_file.txt> [output_directory]

if [ $# -lt 1 ]; then
    echo "Usage: $0 <compressed_file.txt> [output_directory]"
    echo ""
    echo "Example: $0 ./zcert-compressed.txt ./"
    exit 1
fi

COMPRESSED_FILE="$1"
OUTPUT_DIR="${2:-.}"

# Check if file exists
if [ ! -f "$COMPRESSED_FILE" ]; then
    echo "Error: File '$COMPRESSED_FILE' does not exist"
    exit 1
fi

echo "Extracting from: $COMPRESSED_FILE"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Decode from base64 and extract tar.gz
echo "Extracting archive..."
if base64 -d "$COMPRESSED_FILE" | tar -xzf - -C "$OUTPUT_DIR"; then
    FOLDER_NAME=$(base64 -d "$COMPRESSED_FILE" | tar -tzf - | head -1 | cut -d'/' -f1)
    EXTRACTED_PATH="$OUTPUT_DIR/$FOLDER_NAME"
    EXTRACTED_SIZE=$(du -sh "$EXTRACTED_PATH" 2>/dev/null | cut -f1)
    echo "✓ Successfully extracted!"
    echo "  Folder name: $FOLDER_NAME"
    echo "  Extracted size: $EXTRACTED_SIZE"
    echo "  Location: $EXTRACTED_PATH"
else
    echo "✗ Error during extraction"
    exit 1
fi
