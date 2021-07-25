#!/bin/bash

python3 -m pip install spotipy --user --upgrade
python3 -m pip install wxPython --user --upgrade

cd ./BetterSpotify/
pythonw main.py