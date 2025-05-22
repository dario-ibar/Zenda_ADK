#!/bin/bash

# Default values
TIMEOUT=30
PROJECT=""
ZONE=""
INSTANCE=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --timeout) TIMEOUT="$2"; shift ;;
    --project) PROJECT="$2"; shift ;;
    --zone) ZONE="$2"; shift ;;
    --instance) INSTANCE="$2"; shift ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

# Convert timeout to milliseconds (simulate for testing)
TIMEOUT_MS=$((TIMEOUT * 60 * 1000))

# Use dummy idle time (for this environment, as xprintidle may not exist)
IDLE_TIME=0

# Network traffic check
RX_TX=$(cat /proc/net/dev | grep eth0 | awk '{print $2 + $10}')
PREV_FILE="/tmp/.net_activity"

if [ -f "$PREV_FILE" ]; then
  PREV_RX_TX=$(cat $PREV_FILE)
  DELTA=$((RX_TX - PREV_RX_TX))
else
  DELTA=0
fi
echo $RX_TX > $PREV_FILE

# Condition to shutdown
if [[ "$IDLE_TIME" -ge "$TIMEOUT_MS" && "$DELTA" -lt 1000 ]]; then
  echo "Shutting down $INSTANCE after $TIMEOUT minutes of inactivity."
  gcloud compute instances stop "$INSTANCE" --zone="$ZONE" --project="$PROJECT"
else
  echo "Instance active. Idle: $IDLE_TIME ms, Net delta: $DELTA"
fi
