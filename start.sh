#!/bin/bash

export SPOTIPY_CLIENT_ID='ab487ce8b7394857b7131f62e83198be'
export SPOTIPY_CLIENT_SECRET='0c7bd99559c24d0994271fd2efcfe01a'
export SPOTIPY_REDIRECT_URI='http://127.0.0.1/callback'

python3 -m pip install spotipy --user --upgrade
python3 -m pip install wxPython --user --upgrade

cd ./BetterSpotify/
pythonw main.pyw