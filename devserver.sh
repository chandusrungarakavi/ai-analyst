#!/bin/sh
if [ -f .env ]; then
  set -a; source .env; set +a
fi
source .venv/bin/activate
python -u -m flask --app main run -p $PORT --debug
