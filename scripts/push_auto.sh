#!/bin/bash

cd ~/Zenda_ADK || exit 1

# Obtener fecha y hora
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Agregar y commitear si hay cambios
if ! git diff --quiet || ! git diff --cached --quiet; then
    git add .
    git commit -m "Auto-commit: $TIMESTAMP"
    
    # Usar el token para hacer push
    git push https://$GITHUB_TOKEN@github.com/dario-ibar/Zenda_ADK.git main
else
    echo "Sin cambios para commitear - $TIMESTAMP"
fi
