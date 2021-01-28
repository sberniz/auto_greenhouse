#!/bin/bash
set -e
cd /home/pi
gunicorn auto_greenhouse.main:app -b 0.0.0.0:8000 --timeout=120

