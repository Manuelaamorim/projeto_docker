#!/bin/sh
while true; do
  RESPONSE=$(curl -s http://server:8080)
  echo "[CLIENTE] Resposta do servidor: $RESPONSE"
  sleep 3
done
