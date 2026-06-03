#!/bin/bash
# POST MACHINE EXPORT — Launcher macOS
# Duplo clique para iniciar o exportador

cd "$(dirname "$0")"
echo ""
echo "╔══════════════════════════════════════╗"
echo "║   POST MACHINE EXPORT  · Iniciando   ║"
echo "╚══════════════════════════════════════╝"
echo ""

python3 app_exportador.py
