#!/bin/sh
export FLASK_APP=run.py runsever
export FLASK_ENV=development
flask db revision --rev-id 2e7abe5675bf
flask db migrate -m "init"
flask db upgrade
