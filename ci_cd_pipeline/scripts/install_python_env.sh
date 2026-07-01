#!/bin/bash

pip3 install --quiet --no-cache-dir --break-system-packages pytest pylint "$WORKSPACE"/ci_cd_pipeline/requirements.txt
pylint -f parseable "$WORKSPACE"/app | tee pylint.out
