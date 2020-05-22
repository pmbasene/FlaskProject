#!/bin/sh
export FLASK_APP=run.py runsever
export FLASK_ENV=development
flask db revision --rev-id 8c8df735ce3c
flask db migrate -m "init"
flask db upgrade
