#!/bin/bash
set -e
cd /home/pi/auto_greenhouse
FLASK_APP=main.py flask run --host=0.0.0.0


