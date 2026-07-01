#!/bin/bash
set -e

#installa dipendenze
pip3 install --quiet --no-cache-dir --break-system-packages pytest pylint
pip3 install --quiet --no-cache-dir --break-system-packages -r "$WORKSPACE"/ci_cd_pipeline/api/requirements.txt

# esegue pylint
pylint -f parseable "$WORKSPACE"/app | tee pylint.out
