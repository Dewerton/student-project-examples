#!/usr/bin/env bash
set -e

echo -e "\n---Cleaning build folders ---"
for name in 'dist' 'build' '__pycache__' '*.egg-info' 'job-launcher-*' '*.pyz' 'output'; do
  echo "---Trying to clean $name---"
  find . -name "$name" -prune -exec rm -rfv {} \;
done
