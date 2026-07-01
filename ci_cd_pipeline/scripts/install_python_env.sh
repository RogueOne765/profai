#!/bin/bash
set -e

API_SOURCE_PATH="$WORKSPACE"/"ci_cd_pipeline/api"

#installa dipendenze
pip3 install --quiet --no-cache-dir --break-system-packages -r "$API_SOURCE_PATH"/requirements.txt
