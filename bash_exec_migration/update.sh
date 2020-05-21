#!/bin/sh
export FLASK_APP=run.py runsever
export FLASK_ENV=development
flask db migrate -m "update"
flask db upgrade
