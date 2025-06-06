# RECUERDA: Para ejecutar este script EN LA TERMINAL, usa: ./xGitHub_Actual.sh

#!/bin/bash

echo "--- Ejecutando script de actualización de GitHub ---"

# Navegar a la carpeta del proyecto.
# Asume que este script se ejecuta desde el directorio HOME del usuario jupyter (~)
# Si tu carpeta Zenda_ADK está en otro lugar, ajusta esta ruta.
cd ~/Zenda_ADK

# Verificar que estamos en la rama main
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" != "main" ]; then
  echo "Advertencia: No estás en la rama 'main'. El script empujará a la rama actual: $current_branch"
  read -p "¿Deseas continuar? (s/n): " confirm
  if [ "$confirm" != "s" ]; then
    echo "Operación cancelada. Por favor, cambia a la rama 'main' o ajusta el script."
    exit 1
  fi
fi

# Añadir todos los cambios (incluyendo archivos nuevos y eliminados, excluyendo los del .gitignore)
echo "Añadiendo todos los cambios al área de preparación..."
git add .

# Pedir un mensaje de commit al usuario
read -p "Introduce un mensaje para el commit (ej. 'Implementa funcion X'): " commit_message

# Hacer el commit
echo "Realizando commit local..."
git commit -m "$commit_message"

# Empujar los cambios a GitHub
echo "Empujando cambios a GitHub..."
git push origin "$current_branch"

echo "--- Script de actualización de GitHub finalizado ---"