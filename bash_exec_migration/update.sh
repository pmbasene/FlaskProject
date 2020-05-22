#!/bin/sh
export FLASK_APP=run.py runsever
export FLASK_ENV=development
flask db migrate -m $1
flask db upgrade
