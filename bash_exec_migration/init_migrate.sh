#!/bin/sh
export FLASK_APP=run.py runsever
export FLASK_ENV=development
flask db init
flask db migrate -m "init"
flask db upgrade
