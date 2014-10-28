#!/bin/bash

rm -f debug.log
stdbuf -e 0 python3 ./run.py 2>&1 | tee debug.log
