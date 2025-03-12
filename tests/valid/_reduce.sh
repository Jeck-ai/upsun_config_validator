#!/bin/bash

# Loop through all top-level directories
for dir in */; do
  dir=${dir%/}  # Remove trailing slash
  echo "Processing $dir..."

  # Create .upsun directory if it doesn't exist
  mkdir -p "$dir/.upsun"

  # Find the config.yaml file in the files directory
  if [ -f "$dir/files/.upsun/config.yaml" ]; then
    # Copy it to the top-level .upsun directory
    cp "$dir/files/.upsun/config.yaml" "$dir/.upsun/"
    echo "  Copied files/.upsun/config.yaml to .upsun/config.yaml"
  fi

  # Remove everything except the .upsun directory
  find "$dir" -mindepth 1 -maxdepth 1 ! -name ".upsun" -exec rm -rf {} \;
  echo "  Removed all files except .upsun/config.yaml"
done

echo "Clean-up completed successfully!"