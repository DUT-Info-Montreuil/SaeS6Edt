#!/bin/bash

if [[ "$OS" == "Windows_NT" ]]; then
  echo "Le script s'exécute sous Windows."
else
  echo "Le script s'exécute sous un système d'exploitation autre que Windows."
fi