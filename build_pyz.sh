#!/usr/bin/env bash
set -e

echo -e "\n---Update pip---"
pip install -U pip
echo -e "\n---Update setuptools, wheel packages---"
pip install -U setuptools wheel

echo -e "\n---Get job-launcher full name---"
NAME="$(python setup.py --name)"
VERSION="$(python setup.py --version)"
FULLNAME="$(python setup.py --fullname)"
echo "NAME: $NAME"
echo "VERSION: $VERSION"
echo "FULLNAME: $FULLNAME"

echo -e "\n---Build job-launcher python executable archive---"
rm -rfv "$FULLNAME"
pip install -t "$FULLNAME" .
find "$FULLNAME" -type d -regex '.*/__pycache__\|.*\.egg-info' -prune -exec rm -rf {} \;
python -m zipapp "$FULLNAME" --main 'job_launcher.main:main' --python '/usr/bin/env python3' --output "${FULLNAME}.pyz"