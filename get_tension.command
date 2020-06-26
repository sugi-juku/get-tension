#!/bin/sh

cd `dirname $0`
python3 get_tension_app.py
killall Terminal
