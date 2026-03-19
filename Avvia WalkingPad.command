#!/bin/bash
cd "/Users/lorenzochiti/Documents/_1.in atto_P.rojects/LAVORO/SSWS misura"

# Apri il browser dopo 2 secondi (il server ha il tempo di partire)
sleep 2 && open http://localhost:5050 &

# Avvia il server
python3 walkingpad_server.py
