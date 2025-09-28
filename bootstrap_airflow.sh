#!/usr/bin/env bash
set -e
source ~/airflow_dev/venv/bin/activate
airflow db init || true
airflow connections delete slack_default >/dev/null 2>&1 || true
airflow connections add slack_default \
  --conn-type slackwebhook \
  --conn-password "$SLACK_WEBHOOK_URL"
AIRFLOW__CORE__LOAD_EXAMPLES=False airflow standalone
