#!/bin/bash

cd disambiguationApp/

# Comprobar si el proceso "npm start" ya se está ejecutando
if ps aux | grep -v grep | grep "npm start" > /dev/null; then
    echo "El servidor ya se está ejecutando, no se iniciará de nuevo."
else
    npm install --yes --silent
    npm start --yes --silent &
    sleep 5
fi

cd ../disambiguationProgram

./dist/main

cd ..
