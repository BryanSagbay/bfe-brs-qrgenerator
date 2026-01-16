#!/bin/bash

set -e

echo "Inicializando servicios..."

# === RUTAS ===
#Modificar la direccion segun donde tenga el repositorio clonado
PYTHON_DIR="/Users/bryansagbay/Documents/Personal Project/bfe-brs-qrgenerator/neg_qrgenerator"
REACT_DIR="/Users/bryansagbay/Documents/Personal Project/bfe-brs-qrgenerator/pag_qrgenerator"

# === PYTHON ===
echo "Iniciando backend Python..."
cd "$PYTHON_DIR"

# Desactivar conda si existe
if command -v conda &> /dev/null; then
    conda deactivate || true
fi

# Activar entorno virtual
source env/bin/activate

python3 app.py &

# === REACT ===
echo "Iniciando frontend React..."
cd "$REACT_DIR"
npm run dev

wait