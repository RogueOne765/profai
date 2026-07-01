#!/bin/bash

pip3 install --quiet --no-cache-dir --break-system-packages nosexcover pylint "$WORKSPACE"/requirements.txt
nosetests --with-xcoverage --with-xunit --cover-package="$WORKSPACE"/app --cover-erase
pylint -f parseable "$WORKSPACE"/app | tee pylint.out
