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

# Convert timeout to seconds
TIMEOUT_SEC=$((TIMEOUT * 60))

# Simular tiempo de inactividad real (por ahora usaremos solo red)
# Si querés incluir CPU más adelante, se puede ampliar

# Medir actividad de red (entrada + salida)
RX_TX=$(cat /proc/net/dev | grep eth0 | awk '{print $2 + $10}')
PREV_FILE="/tmp/.net_activity"

if [ -f "$PREV_FILE" ]; then
  PREV_RX_TX=$(cat $PREV_FILE)
  DELTA=$((RX_TX - PREV_RX_TX))
else
  PREV_RX_TX=$RX_TX
  DELTA=0
fi

echo $RX_TX > $PREV_FILE

# Verificar si hubo muy poca transferencia
if [[ "$DELTA" -lt 1000 ]]; then
  # Si hubo poca actividad de red durante los últimos 30 minutos, apagamos
  echo "Shutting down $INSTANCE due to inactivity. Net delta: $DELTA"
  gcloud compute instances stop "$INSTANCE" --zone="$ZONE" --project="$PROJECT"
else
  echo "Instance is active. Net delta: $DELTA"
fi
