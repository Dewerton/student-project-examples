#!/usr/bin/env bash
set -e

echo -e "\n---Building job-launcher python packages---"
python setup.py sdist bdist_wheel